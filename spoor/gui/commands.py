"""Turn the GUI's run forms into real `spoor` argument lists (ROADMAP.md §2i, gui-2).

The GUI never re-implements a command: it builds the same argument list a person
would type and runs that (§2i). This module is the one place that mapping lives,
used both to launch a job and to preview its command line, so what the preview
shows is exactly what runs.

Validation is deliberately minimal (§2i gui-2 mechanics decision): only what's
needed to *build* the list — a required field present, a number that is a
number. Everything else (budget bounds, `--screenshots` without `--wiki`, an
output path that is a file, an unknown session) is left to the command itself,
whose error shows up in the job's log. Output paths are made absolute against the
GUI's working directory, so where a job's output landed is never ambiguous.
"""

from __future__ import annotations

import os
import shlex
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path

#: The output formats `spoor run --format` accepts ("" = infer from the file name).
RUN_FORMATS = ("", "json", "jsonl", "csv", "md", "sqlite", "parquet")


class FormError(ValueError):
    """A form can't be turned into a command; the message is shown to the user."""


@dataclass(frozen=True)
class CommandSpec:
    """A command ready to run: its arguments and the outputs it was asked to write."""

    kind: str
    args: list[str]
    # Label → absolute path of every output this command was asked to write.
    outputs: dict[str, Path] = field(default_factory=dict)
    # The URL whose map this command reads or writes, if any.
    map_url: str | None = None

    @property
    def command_line(self) -> str:
        """The command as a person would type it."""
        return "spoor " + shlex.join(self.args)


Form = Mapping[str, str]


def _text(form: Form, name: str) -> str:
    return form.get(name, "").strip()


def _ticked(form: Form, name: str) -> bool:
    return form.get(name, "") not in ("", "off", "false")


def _required(form: Form, name: str, message: str) -> str:
    value = _text(form, name)
    if not value:
        raise FormError(message)
    return value


def _positional(form: Form, name: str, message: str, what: str) -> str:
    """A required value passed as-is as a bare command argument (an address).

    One starting with "-" would be read by the command as an option (typing
    "--sandbox" as the address would tick the sandbox), so it's refused. Paths
    don't need this: they're made absolute first, so they never start with "-".
    """
    value = _required(form, name, message)
    if value.startswith("-"):
        raise FormError(f"{what} can't start with '-'.")
    return value


def _absolute(workdir: Path, value: str) -> Path:
    """`value` as an absolute path, relative paths taken from the GUI's workdir."""
    return Path(os.path.abspath(workdir / Path(value).expanduser()))


def _number(form: Form, name: str, label: str, *, whole: bool) -> str | None:
    """A number field's value as typed (the command parses it), or None if empty."""
    value = _text(form, name)
    if not value:
        return None
    try:
        int(value) if whole else float(value)
    except ValueError:
        kind = "a whole number" if whole else "a number"
        raise FormError(f"{label} must be {kind}.") from None
    return value


def _patterns(form: Form, name: str) -> list[str]:
    """A one-pattern-per-line text area as a list, blank lines skipped."""
    return [line.strip() for line in form.get(name, "").splitlines() if line.strip()]


def _output(
    form: Form,
    workdir: Path,
    *,
    tick: str,
    path_field: str,
    missing: str,
) -> Path | None:
    """An optional output: its absolute path if ticked, else None (path ignored)."""
    if not _ticked(form, tick):
        return None
    return _absolute(workdir, _required(form, path_field, missing))


def explore_command(form: Form, workdir: Path) -> CommandSpec:
    """`spoor explore` from the explore form."""
    url = _positional(
        form, "url", "Enter the address of the site to explore.", "The address"
    )
    args = ["explore", url]
    outputs: dict[str, Path] = {}
    if _ticked(form, "sandbox"):
        args.append("--sandbox")
    for name, flag, label, whole in (
        ("max_states", "--max-states", "Max screens", True),
        ("max_requests", "--max-requests", "Max actions", True),
        ("max_seconds", "--max-seconds", "Time limit", False),
        ("max_depth", "--max-depth", "Max depth", True),
    ):
        value = _number(form, name, label, whole=whole)
        if value is not None:
            args += [flag, value]
    for name, flag in (("resume_from", "--resume-from"), ("session", "--session")):
        value = _text(form, name)
        if value:
            args += [flag, value]
    wiki = _output(
        form, workdir, tick="wiki", path_field="wiki_dir",
        missing="Choose a folder for the wiki.",
    )
    if wiki is not None:
        args += ["--wiki", str(wiki)]
        outputs["wiki"] = wiki
    if _ticked(form, "screenshots"):
        args.append("--screenshots")
    tests = _output(
        form, workdir, tick="gen_tests", path_field="gen_tests_dir",
        missing="Choose a folder for the generated tests.",
    )
    if tests is not None:
        args += ["--gen-tests", str(tests)]
        outputs["tests"] = tests
    if _ticked(form, "assert_no_new_signals"):
        args.append("--assert-no-new-signals")
    scaffold = _output(
        form, workdir, tick="scaffold", path_field="scaffold_dir",
        missing="Choose a folder for the scaffold.",
    )
    if scaffold is not None:
        args += ["--scaffold", str(scaffold)]
        outputs["scaffold"] = scaffold
    for name, flag in (
        ("include_elements", "--include-element"),
        ("exclude_elements", "--exclude-element"),
    ):
        for pattern in _patterns(form, name):
            args += [flag, pattern]
    return CommandSpec("explore", args, outputs, map_url=url)


def run_command(form: Form, workdir: Path) -> CommandSpec:
    """`spoor run` from the extraction form."""
    config = _absolute(
        workdir,
        _required(form, "config", "Choose the config file to run."),
    )
    output = _absolute(
        workdir, _required(form, "output", "Choose where to write the records.")
    )
    args = ["run", str(config), "--output", str(output)]
    outputs = {"output": output}
    fmt = _text(form, "format")
    if fmt not in RUN_FORMATS:
        raise FormError(f"Unknown output format {fmt!r}.")
    if fmt:
        args += ["--format", fmt]
    report = _output(
        form, workdir, tick="healing_report", path_field="healing_report_path",
        missing="Choose where to write the healing report.",
    )
    if report is not None:
        args += ["--healing-report", str(report)]
        outputs["healing report"] = report
    return CommandSpec("run", args, outputs)


def apply_scaffold_command(form: Form, workdir: Path) -> CommandSpec:
    """`spoor apply-scaffold` from the apply-scaffold form."""
    url = _positional(
        form, "url", "Enter the address of the mapped page.", "The address"
    )
    scaffold = _absolute(
        workdir,
        _required(form, "scaffold", "Enter the path of the filled-in scaffold file."),
    )
    args = ["apply-scaffold", url, str(scaffold)]
    outputs: dict[str, Path] = {}
    if _ticked(form, "sandbox"):
        args.append("--sandbox")
    session = _text(form, "session")
    if session:
        args += ["--session", session]
    wiki = _output(
        form, workdir, tick="wiki", path_field="wiki_dir",
        missing="Choose the wiki folder to refresh.",
    )
    if wiki is not None:
        args += ["--wiki", str(wiki)]
        outputs["wiki"] = wiki
    return CommandSpec("apply-scaffold", args, outputs, map_url=url)


#: Form kind (as used in the GUI's URLs) → its command builder.
BUILDERS: dict[str, Callable[[Form, Path], CommandSpec]] = {
    "explore": explore_command,
    "run": run_command,
    "apply-scaffold": apply_scaffold_command,
}
