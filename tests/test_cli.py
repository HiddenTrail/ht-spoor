"""End-to-end CLI tests for `spoor run` output wiring (ROADMAP.md §2a, §2d) and
`spoor wizard` (interactive command building).

`extract.run_report` is monkeypatched to a fixed `RunResult` so the CLI surface —
format selection, the output pipeline, and the run summary — is exercised without
any network. The wizard tests drive `typer.prompt`/`typer.confirm` via `CliRunner`'s
`input=`, exactly as the prompts themselves would read from a real terminal.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from typer.testing import CliRunner

from spoor import cli
from spoor.core import extract
from spoor.core.extract import RunResult

runner = CliRunner()


def _flatten_cli_error(output: str) -> str:
    """Strip a CLI error down to its bare characters for a formatting-robust assertion.

    Typer renders a `BadParameter` through Rich into a bordered, ANSI-coloured panel
    wrapped to the terminal width. Across Rich versions the wrap can split a token like
    `--wiki` across the panel border, so a naive `"--wiki" in output` passes on one
    machine and fails on another (this bit CI once). Removing the ANSI codes, the
    box-drawing borders, and all whitespace rejoins the message text regardless of how
    it was wrapped, so a substring check tests the *message*, not the rendering.
    """
    no_ansi = re.sub(r"\x1b\[[0-9;]*m", "", output)
    return re.sub(r"[\s─-╿]", "", no_ansi)


def _stub_result() -> RunResult:
    return RunResult(
        records=[{"title": "A", "price": 1.0}],
        tier=1,
        pages_fetched=1,
        tiers_attempted=[1],
    )


_CONFIG = """
target: http://localhost:8000/x.html
fields:
  title: { selector: "h1" }
  price: { selector: ".price", type: number }
"""


def _config_file(tmp_path: Path) -> Path:
    path = tmp_path / "config.yaml"
    path.write_text(_CONFIG, encoding="utf-8")
    return path


def test_run_infers_csv_from_extension(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(extract, "run_report", lambda cfg: _stub_result())
    out = tmp_path / "out.csv"
    result = runner.invoke(
        cli.app, ["run", str(_config_file(tmp_path)), "-o", str(out)]
    )
    assert result.exit_code == 0, result.output
    assert out.read_text(encoding="utf-8").splitlines()[0] == "title,price"


def test_run_format_override(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(extract, "run_report", lambda cfg: _stub_result())
    out = tmp_path / "out.dat"
    result = runner.invoke(
        cli.app,
        ["run", str(_config_file(tmp_path)), "-o", str(out), "-f", "json"],
    )
    assert result.exit_code == 0, result.output
    assert json.loads(out.read_text(encoding="utf-8")) == [{"title": "A", "price": 1.0}]


def test_bad_format_aborts_before_extraction(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls = {"n": 0}

    def _record_call(cfg: object) -> RunResult:
        calls["n"] += 1
        return RunResult()

    monkeypatch.setattr(extract, "run_report", _record_call)
    out = tmp_path / "out.dat"  # unknown extension, no --format
    result = runner.invoke(
        cli.app, ["run", str(_config_file(tmp_path)), "-o", str(out)]
    )
    assert result.exit_code != 0
    assert calls["n"] == 0  # format is resolved before anything is fetched
    assert not out.exists()


def test_explore_screenshots_requires_wiki(monkeypatch: pytest.MonkeyPatch) -> None:
    # --screenshots without --wiki is rejected before any browser is launched: there is
    # nowhere to put the images (§2e slice 8b). Guard against ever starting a driver.
    from spoor.exploration import driver as driver_mod

    def _boom(*_a: object, **_k: object) -> object:
        raise AssertionError("a browser must not be launched when the flag is rejected")

    monkeypatch.setattr(driver_mod, "PlaywrightDriver", _boom)
    result = runner.invoke(
        cli.app, ["explore", "http://localhost:8000/", "--screenshots"]
    )
    assert result.exit_code != 0
    # The error must name --wiki so the user knows what to add; assert on the flattened
    # message so a Rich panel line-wrap (differs across environments) can't hide it.
    assert "--wiki" in _flatten_cli_error(result.output)


def test_explore_resume_without_saved_map_aborts_before_browser(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # --resume-from on a URL that was never mapped is rejected before any browser is
    # launched: there is no saved map to continue (§2e resume). An empty cache root
    # guarantees the URL is unmapped whatever else is on the machine.
    from spoor.exploration import driver as driver_mod
    from spoor.security import storage

    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path)

    def _boom(*_a: object, **_k: object) -> object:
        raise AssertionError("a browser must not be launched with no map to resume")

    monkeypatch.setattr(driver_mod, "PlaywrightDriver", _boom)
    result = runner.invoke(
        cli.app,
        ["explore", "http://localhost:8000/", "--resume-from", "id:abc123"],
    )
    assert result.exit_code != 0
    # The message must point the user at mapping the URL first. Assert on the flattened
    # (whitespace-stripped) message so a Rich panel line-wrap can't hide the token.
    assert "nosavedexplorationmap" in _flatten_cli_error(result.output)


# --- wizard --------------------------------------------------------------------


def test_wizard_declining_run_prints_command_and_does_not_execute(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[list[str]] = []
    monkeypatch.setattr("subprocess.run", lambda argv, **_k: calls.append(argv))
    # 1=explore, url, sandbox=n, states/requests/seconds blank, depth=2, resume
    # blank, wiki=./wiki, screenshots=n, gen-tests/scaffold blank, run-now=n.
    answers = "1\nhttp://localhost:8000/\nn\n\n\n\n2\n\n./wiki\nn\n\n\nn\n"
    result = runner.invoke(cli.app, ["wizard"], input=answers)
    assert result.exit_code == 0, result.output
    assert calls == []
    assert "spoor explore http://localhost:8000/ --max-depth 2 --wiki ./wiki" in (
        result.output
    )
    assert "--sandbox" not in result.output.split("Resolved command:")[1]


def test_wizard_confirming_run_invokes_the_resolved_command(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import sys

    calls: list[list[str]] = []

    def _record(argv: list[str], **_kwargs: object) -> None:
        calls.append(argv)

    monkeypatch.setattr("subprocess.run", _record)
    answers = "1\nhttp://localhost:8000/\ny\n\n\n\n\n\n\n\n\ny\n"
    result = runner.invoke(cli.app, ["wizard"], input=answers)
    assert result.exit_code == 0, result.output
    assert calls == [
        [
            sys.executable,
            "-m",
            "spoor.cli",
            "explore",
            "http://localhost:8000/",
            "--sandbox",
        ]
    ]


def test_wizard_reprompts_on_a_non_numeric_answer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[list[str]] = []
    monkeypatch.setattr("subprocess.run", lambda argv, **_k: calls.append(argv))
    # max-states gets a bad answer ("abc") once before a good one ("5").
    answers = "1\nhttp://localhost:8000/\nn\nabc\n5\n\n\n\n\n\n\n\nn\n"
    result = runner.invoke(cli.app, ["wizard"], input=answers)
    assert result.exit_code == 0, result.output
    assert "isn't a whole number" in result.output
    assert "--max-states 5" in result.output


def test_wizard_apply_scaffold_builds_the_right_command(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[list[str]] = []
    monkeypatch.setattr("subprocess.run", lambda argv, **_k: calls.append(argv))
    # 2=apply-scaffold, url, scaffold path, sandbox=y, wiki blank, run-now=n.
    answers = "2\nhttp://localhost:5173\n./interactive.yaml\ny\n\nn\n"
    result = runner.invoke(cli.app, ["wizard"], input=answers)
    assert result.exit_code == 0, result.output
    assert calls == []
    assert (
        "spoor apply-scaffold http://localhost:5173 ./interactive.yaml --sandbox"
        in result.output
    )
