"""The fake command runner shared by the GUI's step definitions (ROADMAP.md §2i).

Stands in for the subprocess a GUI job runs: it records what it was asked to
start (arguments and environment) and plays a scripted process, so the GUI's
command building, logs, Stop and output handling are tested without launching
Spoor. Not a step module itself: it defines no `@given/@when/@then`.
"""

from __future__ import annotations

import queue
import threading
from collections.abc import Callable, Mapping, Sequence
from typing import Any

#: How long a fake process (or a step waiting on one) waits before giving up.
FINISH_TIMEOUT_S = 10.0


class FakeProcess:
    """A scripted stand-in for a child process."""

    def __init__(self) -> None:
        self._lines: queue.Queue[str | None] = queue.Queue()
        self._done = threading.Event()
        self.killed = threading.Event()
        self.exit_code = 0

    def emit(self, line: str) -> None:
        self._lines.put(line + "\n")

    def exit(self, code: int) -> None:
        self.exit_code = code
        self._lines.put(None)
        self._done.set()

    def readline(self) -> str:
        line = self._lines.get(timeout=FINISH_TIMEOUT_S)
        return "" if line is None else line

    def wait(self) -> int:
        self._done.wait(FINISH_TIMEOUT_S)
        return self.exit_code

    def kill(self) -> None:
        self.killed.set()


Script = Callable[[FakeProcess, Sequence[str], Mapping[str, str]], None]


def _exit_at_once(proc: FakeProcess, args: Sequence[str], env: Any) -> None:
    proc.exit(0)


class FakeRunner:
    """Records every start and runs the current script in a thread."""

    def __init__(self) -> None:
        self.started: list[tuple[list[str], dict[str, str]]] = []
        self.processes: list[FakeProcess] = []
        self.script: Script = _exit_at_once

    def start(self, args: Sequence[str], env: Mapping[str, str]) -> FakeProcess:
        self.started.append((list(args), dict(env)))
        proc = FakeProcess()
        self.processes.append(proc)
        threading.Thread(
            target=self.script, args=(proc, list(args), dict(env)), daemon=True
        ).start()
        return proc


def flag_value(args: Sequence[str], flag: str) -> str:
    return args[args.index(flag) + 1]
