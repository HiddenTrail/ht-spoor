"""Run and supervise `spoor` commands started from the GUI (ROADMAP.md §2i, gui-2).

A job is one real CLI invocation (`python -m spoor.cli <args>`) in a child
process. The manager keeps its redacted output, its status, and the outputs it
was asked to write, and it can stop it:

- **Stop** for `explore` is graceful. The job's environment names a stop file
  (`SPOOR_STOP_FILE`); creating it makes `explore` finish its current action,
  save what it mapped and write its outputs, exactly as Ctrl-C does in a
  terminal. A file, not a signal, because on Windows a console signal also hits
  Playwright's own processes and crashes the run instead of stopping it.
- **Force stop** (and Stop for `run`/`apply-scaffold`, which have no graceful
  stop) kills the job's whole process tree, so no orphaned browser is left.

Every output line goes through the §2h `redact` primitive before it is stored,
so a secret a command prints never reaches the page. The runner is injectable so
tests can supervise a fake process instead of launching Spoor.
"""

from __future__ import annotations

import os
import secrets
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from collections import deque
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol

from spoor.gui.commands import CommandSpec
from spoor.security.redaction import redact

#: How many log lines a job keeps; older lines are dropped (and counted).
MAX_LOG_LINES = 10_000

#: Kinds whose Stop is graceful (the command honors SPOOR_STOP_FILE).
GRACEFUL_KINDS = frozenset({"explore"})


class RunningProcess(Protocol):
    """The slice of a child process the manager needs."""

    def readline(self) -> str:
        """The next output line, or "" once the process has closed its output."""
        ...

    def wait(self) -> int:
        """Block until the process exits; its exit code."""
        ...

    def kill(self) -> None:
        """End the process and everything it started, immediately."""
        ...


class Runner(Protocol):
    """Starts a `spoor` command with extra environment variables."""

    def start(self, args: Sequence[str], env: Mapping[str, str]) -> RunningProcess:
        ...


class _Subprocess:
    """A real child process, merged stdout/stderr, killable as a tree."""

    def __init__(self, popen: subprocess.Popen[str]) -> None:
        self._popen = popen

    def readline(self) -> str:
        assert self._popen.stdout is not None
        return self._popen.stdout.readline()

    def wait(self) -> int:
        return self._popen.wait()

    def kill(self) -> None:
        if self._popen.poll() is not None:
            return
        if sys.platform == "win32":
            # /T takes the whole tree: Playwright's driver and Chromium too.
            subprocess.run(
                ["taskkill", "/PID", str(self._popen.pid), "/T", "/F"],
                capture_output=True,
                check=False,
            )
        else:
            try:
                # The child leads its own session (start_new_session), so its
                # process group is exactly the job's tree.
                os.killpg(self._popen.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass


class SubprocessRunner:
    """Runs `python -m spoor.cli <args>` in `cwd` — the real CLI, nothing else."""

    def __init__(self, cwd: Path) -> None:
        self._cwd = cwd

    def start(self, args: Sequence[str], env: Mapping[str, str]) -> RunningProcess:
        child_env = {
            **os.environ,
            **env,
            # Line-by-line output in UTF-8, whatever the console code page is.
            "PYTHONUNBUFFERED": "1",
            "PYTHONIOENCODING": "utf-8",
        }
        kwargs: dict[str, object] = {}
        if sys.platform == "win32":
            # Keep the GUI terminal's Ctrl+C from reaching the child directly;
            # the GUI stops its jobs itself on shutdown.
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            kwargs["start_new_session"] = True
        popen = subprocess.Popen(  # noqa: S603 - fixed interpreter + our own CLI
            [sys.executable, "-m", "spoor.cli", *args],
            cwd=self._cwd,
            env=child_env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            **kwargs,  # type: ignore[call-overload]
        )
        return _Subprocess(popen)


@dataclass
class Job:
    """One supervised command and everything the GUI shows about it."""

    id: str
    spec: CommandSpec
    stop_file: Path
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    status: str = "running"  # running | succeeded | failed | stopped
    exit_code: int | None = None
    finished_at: datetime | None = None
    stop_requested: bool = False
    killed: bool = False
    lines: deque[str] = field(default_factory=lambda: deque(maxlen=MAX_LOG_LINES))
    total_lines: int = 0
    process: RunningProcess | None = None
    # Guards `lines` + `total_lines` together, so a reader never sees one updated
    # without the other.
    log_lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    @property
    def graceful_stop(self) -> bool:
        return self.spec.kind in GRACEFUL_KINDS

    @property
    def running(self) -> bool:
        return self.status == "running"

    def lines_from(self, start: int) -> tuple[int, list[str]]:
        """Lines numbered `start` onward still held, and the number after them.

        Line numbers count every line the job ever printed, so a reader that
        asks again from where it left off never sees a line twice, even after
        the oldest lines were dropped.
        """
        with self.log_lock:
            snapshot = list(self.lines)
            total = self.total_lines
        first = total - len(snapshot)
        start = min(max(start, first), total)
        return total, snapshot[start - first :]


class JobManager:
    """Starts, tracks and stops jobs for one GUI process."""

    def __init__(self, runner: Runner, workdir: Path) -> None:
        self.runner = runner
        #: Where relative paths in a form are taken from, and where jobs run.
        self.workdir = workdir
        self._jobs: dict[str, Job] = {}
        self._lock = threading.Lock()
        #: How long `run_and_wait` lets a short command run before stopping it.
        self.quick_command_seconds = 30.0
        # Created on the first job, removed on shutdown.
        self._stop_dir: Path | None = None

    def start(self, spec: CommandSpec) -> Job:
        with self._lock:
            if self._stop_dir is None:
                self._stop_dir = Path(tempfile.mkdtemp(prefix="spoor-gui-"))
            job_id = secrets.token_hex(4)
            while job_id in self._jobs:
                job_id = secrets.token_hex(4)
            job = Job(job_id, spec, self._stop_dir / f"{job_id}.stop")
            self._jobs[job_id] = job
        env = {"SPOOR_PROGRESS": "lines", "SPOOR_STOP_FILE": str(job.stop_file)}
        try:
            job.process = self.runner.start(spec.args, env)
        except OSError as exc:
            self._append(job, f"Could not start the command: {exc}")
            self._finish(job, None)
            return job
        threading.Thread(target=self._pump, args=(job,), daemon=True).start()
        return job

    def run_and_wait(self, spec: CommandSpec) -> tuple[Job, bool]:
        """Run a short command (e.g. `spoor session add`) and wait for it.

        Waits at most `quick_command_seconds`; a command still running then is
        force-stopped. Returns the job and whether it finished in time.
        """
        job = self.start(spec)
        deadline = time.monotonic() + self.quick_command_seconds
        while job.running and time.monotonic() < deadline:
            time.sleep(0.02)
        if not job.running:
            return job, True
        self.kill(job)
        grace = time.monotonic() + 5.0
        while job.running and time.monotonic() < grace:
            time.sleep(0.02)
        return job, False

    def get(self, job_id: str) -> Job | None:
        return self._jobs.get(job_id)

    def all(self) -> list[Job]:
        """Every job started in this GUI session, newest first."""
        return sorted(self._jobs.values(), key=lambda j: j.started_at, reverse=True)

    def stop(self, job: Job) -> None:
        """Graceful stop where the command supports it, otherwise Force stop."""
        if not job.running:
            return
        if job.graceful_stop:
            job.stop_requested = True
            job.stop_file.touch()
        else:
            self.kill(job)

    def kill(self, job: Job) -> None:
        """Force stop: end the job's whole process tree now."""
        if not job.running or job.process is None:
            return
        job.killed = True
        job.process.kill()

    def shutdown(self) -> None:
        """Force-stop every running job and remove the stop files (GUI closing)."""
        for job in self.all():
            self.kill(job)
        if self._stop_dir is not None:
            shutil.rmtree(self._stop_dir, ignore_errors=True)

    def _append(self, job: Job, line: str) -> None:
        # A stray carriage return (a redrawn progress bar) would split one line in
        # two in the live log's event stream, so it is dropped first.
        redacted = redact(line.replace("\r", ""))
        with job.log_lock:
            job.lines.append(redacted)
            job.total_lines += 1

    def _pump(self, job: Job) -> None:
        process = job.process
        assert process is not None
        for line in iter(process.readline, ""):
            self._append(job, line.rstrip("\r\n"))
        self._finish(job, process.wait())

    def _finish(self, job: Job, exit_code: int | None) -> None:
        job.exit_code = exit_code
        job.finished_at = datetime.now(UTC)
        if exit_code == 0:
            # A clean exit after Stop is a graceful stop; a clean exit that beat a
            # Force stop to it simply finished.
            job.status = "stopped" if job.stop_requested else "succeeded"
        elif job.killed:
            job.status = "stopped"
        else:
            job.status = "failed"


def open_folder(path: Path) -> None:
    """Open `path` (a folder, or the folder a file is in) in the system file browser."""
    folder = path if path.is_dir() else path.parent
    if sys.platform == "win32":
        os.startfile(folder)  # noqa: S606
    elif sys.platform == "darwin":
        subprocess.run(["open", str(folder)], check=False)
    else:
        subprocess.run(["xdg-open", str(folder)], check=False)
