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


def test_run_writes_healing_report_when_something_healed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from spoor.core.self_healing import HealEvent

    def _healed_result(cfg: object) -> RunResult:
        result = _stub_result()
        result.heal_events = [
            HealEvent(
                field="price",
                confidence=0.91,
                used=True,
                old_selector=".price-old",
                new_locator=".price-new",
            )
        ]
        return result

    monkeypatch.setattr(extract, "run_report", _healed_result)
    out = tmp_path / "out.json"
    report_path = tmp_path / "healing.md"
    result = runner.invoke(
        cli.app,
        [
            "run",
            str(_config_file(tmp_path)),
            "-o",
            str(out),
            "--healing-report",
            str(report_path),
        ],
    )
    assert result.exit_code == 0, result.output
    assert report_path.exists()
    report = report_path.read_text(encoding="utf-8")
    assert "price" in report
    assert ".price-old" in report
    assert ".price-new" in report
    assert str(report_path) in result.output


def test_run_healing_report_skipped_when_nothing_healed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(extract, "run_report", lambda cfg: _stub_result())
    out = tmp_path / "out.json"
    report_path = tmp_path / "healing.md"
    result = runner.invoke(
        cli.app,
        [
            "run",
            str(_config_file(tmp_path)),
            "-o",
            str(out),
            "--healing-report",
            str(report_path),
        ],
    )
    assert result.exit_code == 0, result.output
    assert not report_path.exists()
    assert "nothing healed" in result.output


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


def test_explore_assert_no_new_signals_requires_gen_tests(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # --assert-no-new-signals without --gen-tests is rejected before any browser is
    # launched: there is no generated suite to add the check to (closes #128).
    from spoor.exploration import driver as driver_mod

    def _boom(*_a: object, **_k: object) -> object:
        raise AssertionError("a browser must not be launched when the flag is rejected")

    monkeypatch.setattr(driver_mod, "PlaywrightDriver", _boom)
    result = runner.invoke(
        cli.app, ["explore", "http://localhost:8000/", "--assert-no-new-signals"]
    )
    assert result.exit_code != 0
    assert "--gen-tests" in _flatten_cli_error(result.output)


def test_explore_assert_no_new_signals_is_threaded_into_render_suite(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from spoor.exploration import driver as driver_mod
    from spoor.exploration.graph import ExplorationGraph

    class _FakeDriver:
        def __init__(self, target: str, **_kwargs: object) -> None:
            pass

        def __enter__(self) -> _FakeDriver:
            return self

        def __exit__(self, *exc: object) -> None:
            pass

    seen: dict[str, object] = {}

    def _fake_render_suite(*_a: object, **kwargs: object) -> list[Path]:
        seen["assert_no_new_signals"] = kwargs["assert_no_new_signals"]
        return []

    monkeypatch.setattr(driver_mod, "PlaywrightDriver", _FakeDriver)
    monkeypatch.setattr(
        "spoor.exploration.explorer.explore", lambda *a, **k: ExplorationGraph()
    )
    monkeypatch.setattr("spoor.testgen.render_suite", _fake_render_suite)
    result = runner.invoke(
        cli.app,
        [
            "explore",
            "http://localhost:8000/",
            "--gen-tests",
            str(tmp_path / "suite"),
            "--assert-no-new-signals",
        ],
    )
    assert result.exit_code == 0, result.output
    assert seen["assert_no_new_signals"] is True


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


def test_explore_bad_session_aborts_before_browser(tmp_path: Path) -> None:
    # A missing --session file is rejected before any browser is launched, the
    # same posture --resume-from and --screenshots already take (ROADMAP.md §2h).
    from spoor.exploration import driver as driver_mod

    def _boom(*_a: object, **_k: object) -> object:
        raise AssertionError("a browser must not be launched with a bad session")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(driver_mod, "PlaywrightDriver", _boom)
        result = runner.invoke(
            cli.app,
            [
                "explore",
                "http://localhost:8000/",
                "--session",
                str(tmp_path / "does-not-exist.json"),
            ],
        )
    assert result.exit_code != 0
    assert "sessionfile" in _flatten_cli_error(result.output).lower()


def test_explore_session_is_threaded_into_the_driver(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A valid --session reaches PlaywrightDriver's own session kwarg, not just
    # past the up-front check.
    from spoor.exploration import driver as driver_mod

    session_file = tmp_path / "session.json"
    session_file.write_text('{"cookies": [], "origins": []}', encoding="utf-8")
    seen: dict[str, object] = {}

    class _FakeDriver:
        def __init__(self, target: str, *, session: str | None = None) -> None:
            seen["target"] = target
            seen["session"] = session

        def __enter__(self) -> _FakeDriver:
            return self

        def __exit__(self, *exc: object) -> None:
            pass

    from spoor.exploration.graph import ExplorationGraph

    monkeypatch.setattr(driver_mod, "PlaywrightDriver", _FakeDriver)
    monkeypatch.setattr(
        "spoor.exploration.explorer.explore", lambda *a, **k: ExplorationGraph()
    )
    result = runner.invoke(
        cli.app,
        ["explore", "http://localhost:8000/", "--session", str(session_file)],
    )
    assert result.exit_code == 0, result.output
    assert seen["session"] == str(session_file)


def test_apply_scaffold_session_is_threaded_into_the_driver(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from spoor.exploration import driver as driver_mod
    from spoor.exploration.graph import ExplorationGraph
    from spoor.security import storage
    from spoor.serving.store import MapStore, shareable_exploration_map

    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path)
    url = "http://localhost:8000/"
    graph = ExplorationGraph()
    graph.add_state("s1", [])
    MapStore().record(url, [], exploration=shareable_exploration_map(graph))
    scaffold_file = tmp_path / "interactive.yaml"
    scaffold_file.write_text("fields: []\n", encoding="utf-8")
    session_file = tmp_path / "session.json"
    session_file.write_text('{"cookies": [], "origins": []}', encoding="utf-8")
    seen: dict[str, object] = {}

    class _FakeDriver:
        def __init__(self, target: str, *, session: str | None = None) -> None:
            seen["session"] = session

        def __enter__(self) -> _FakeDriver:
            return self

        def __exit__(self, *exc: object) -> None:
            pass

    monkeypatch.setattr(driver_mod, "PlaywrightDriver", _FakeDriver)
    monkeypatch.setattr(
        "spoor.scaffold.apply.apply_scaffold", lambda *a, **k: ([], [])
    )
    result = runner.invoke(
        cli.app,
        [
            "apply-scaffold",
            url,
            str(scaffold_file),
            "--session",
            str(session_file),
        ],
    )
    assert result.exit_code == 0, result.output
    assert seen["session"] == str(session_file)


def test_explore_include_element_patterns_from_file_are_threaded_in(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # --include-element/--exclude-element @<file> reads one pattern per line
    # (blank lines and '#' comments skipped), mixing freely with literal patterns
    # given via repeated flags (§2e, #152 follow-up).
    from spoor.exploration import driver as driver_mod
    from spoor.exploration.element_rules import ElementRules
    from spoor.exploration.graph import ExplorationGraph

    patterns_file = tmp_path / "rules.txt"
    patterns_file.write_text(
        "# a comment\nAdd to cart*\n\nCheckout*\n", encoding="utf-8"
    )

    class _FakeDriver:
        def __init__(self, target: str, **_kwargs: object) -> None:
            pass

        def __enter__(self) -> _FakeDriver:
            return self

        def __exit__(self, *exc: object) -> None:
            pass

    seen: dict[str, object] = {}

    def _fake_explore(*_a: object, **kwargs: object) -> ExplorationGraph:
        seen["element_rules"] = kwargs["element_rules"]
        return ExplorationGraph()

    monkeypatch.setattr(driver_mod, "PlaywrightDriver", _FakeDriver)
    monkeypatch.setattr("spoor.exploration.explorer.explore", _fake_explore)
    result = runner.invoke(
        cli.app,
        [
            "explore",
            "http://localhost:8000/",
            "--include-element",
            f"@{patterns_file}",
            "--include-element",
            "Buy Now*",
        ],
    )
    assert result.exit_code == 0, result.output
    rules = seen["element_rules"]
    assert isinstance(rules, ElementRules)
    assert rules.include == ("Add to cart*", "Checkout*", "Buy Now*")
    assert rules.exclude is None


def test_explore_missing_element_patterns_file_aborts_before_browser(
    tmp_path: Path,
) -> None:
    from spoor.exploration import driver as driver_mod

    def _boom(*_a: object, **_k: object) -> object:
        raise AssertionError("a browser must not be launched with a bad patterns file")

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(driver_mod, "PlaywrightDriver", _boom)
        result = runner.invoke(
            cli.app,
            [
                "explore",
                "http://localhost:8000/",
                "--include-element",
                f"@{tmp_path / 'does-not-exist.txt'}",
            ],
        )
    assert result.exit_code != 0
    assert "couldnotreadfile" in _flatten_cli_error(result.output).lower()


def test_explore_empty_element_patterns_file_aborts_before_browser(
    tmp_path: Path,
) -> None:
    from spoor.exploration import driver as driver_mod

    patterns_file = tmp_path / "empty.txt"
    patterns_file.write_text("# just a comment\n\n", encoding="utf-8")

    def _boom(*_a: object, **_k: object) -> object:
        raise AssertionError(
            "a browser must not be launched with an empty patterns file"
        )

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(driver_mod, "PlaywrightDriver", _boom)
        result = runner.invoke(
            cli.app,
            [
                "explore",
                "http://localhost:8000/",
                "--exclude-element",
                f"@{patterns_file}",
            ],
        )
    assert result.exit_code != 0
    assert "containsnopatterns" in _flatten_cli_error(result.output).lower()


def _explore_with_skips(monkeypatch: pytest.MonkeyPatch, reasons: list[str]) -> str:
    """Run `explore` against a fake driver whose graph has one skip per reason."""
    from spoor.exploration import driver as driver_mod
    from spoor.exploration.discovery import ActionableElement
    from spoor.exploration.graph import ExplorationGraph

    class _FakeDriver:
        def __init__(self, target: str, **_kwargs: object) -> None:
            pass

        def __enter__(self) -> _FakeDriver:
            return self

        def __exit__(self, *exc: object) -> None:
            pass

    graph = ExplorationGraph()
    graph.add_state("s1", [])
    for i, reason in enumerate(reasons):
        graph.record_skip("s1", ActionableElement("button", f"b{i}", None), reason)

    monkeypatch.setattr(driver_mod, "PlaywrightDriver", _FakeDriver)
    monkeypatch.setattr("spoor.exploration.explorer.explore", lambda *a, **k: graph)
    result = runner.invoke(cli.app, ["explore", "http://localhost:8000/"])
    assert result.exit_code == 0, result.output
    return result.output


def test_actuation_failure_skips_are_not_reported_as_destructive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # A skip whose reason has nothing to do with the safety gate (an element that
    # could not be relocated after replay) must not be blamed on "not a sandbox" --
    # DESTRUCTIVE_SKIP_REASON exists precisely so this distinction isn't lost.
    output = _explore_with_skips(
        monkeypatch,
        ["could not be performed: button 'play' not located after replay"],
    )
    assert "destructive" not in output
    assert "could not be reached or performed after replay" in output


def test_destructive_skips_are_still_reported(monkeypatch: pytest.MonkeyPatch) -> None:
    from spoor.exploration.safety import DESTRUCTIVE_SKIP_REASON

    output = _explore_with_skips(monkeypatch, [DESTRUCTIVE_SKIP_REASON])
    assert "1 destructive, skipped" in output
    assert "could not be reached" not in output


def test_a_mix_of_skip_reasons_reports_both(monkeypatch: pytest.MonkeyPatch) -> None:
    from spoor.exploration.safety import DESTRUCTIVE_SKIP_REASON

    output = _explore_with_skips(
        monkeypatch,
        [
            DESTRUCTIVE_SKIP_REASON,
            "could not be performed: button 'play' not located after replay",
            "could not be performed: button 'mute' not located after replay",
        ],
    )
    assert "1 destructive, skipped" in output
    assert "2 could not be reached or performed after replay" in output


# --- wizard --------------------------------------------------------------------


def test_wizard_declining_run_prints_command_and_does_not_execute(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[list[str]] = []
    monkeypatch.setattr("subprocess.run", lambda argv, **_k: calls.append(argv))
    # 1=explore, url, sandbox=n, states/requests/seconds blank, depth=2, resume
    # blank, session blank, wiki=./wiki, screenshots=n, gen-tests/scaffold blank,
    # run-now=n.
    answers = "1\nhttp://localhost:8000/\nn\n\n\n\n2\n\n\n./wiki\nn\n\n\nn\n"
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
    answers = "1\nhttp://localhost:8000/\ny\n\n\n\n\n\n\n\n\n\ny\n"
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
    answers = "1\nhttp://localhost:8000/\nn\nabc\n5\n\n\n\n\n\n\n\n\nn\n"
    result = runner.invoke(cli.app, ["wizard"], input=answers)
    assert result.exit_code == 0, result.output
    assert "isn't a whole number" in result.output
    assert "--max-states 5" in result.output


def test_wizard_apply_scaffold_builds_the_right_command(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[list[str]] = []
    monkeypatch.setattr("subprocess.run", lambda argv, **_k: calls.append(argv))
    # 2=apply-scaffold, url, scaffold path, sandbox=y, session blank, wiki blank,
    # run-now=n.
    answers = "2\nhttp://localhost:5173\n./interactive.yaml\ny\n\n\nn\n"
    result = runner.invoke(cli.app, ["wizard"], input=answers)
    assert result.exit_code == 0, result.output
    assert calls == []
    assert (
        "spoor apply-scaffold http://localhost:5173 ./interactive.yaml --sandbox"
        in result.output
    )


# --- output-path validation ------------------------------------------------
#
# --scaffold now writes into a directory (interactive.yaml inside it), the same
# as --wiki/--gen-tests, rather than taking a file path directly -- closing the
# gap that let a real incident happen: --wiki and --scaffold given the same path
# used to crash mid-crawl, because --scaffold expected a file where --wiki had
# already created a directory. Now all three write non-colliding filenames into
# whatever directory they're given, so sharing one is fine and no longer flagged;
# what's still wrong is any of them pointing at a path that already exists as
# something other than a directory.


def test_explore_allows_wiki_and_scaffold_sharing_a_directory() -> None:
    cli._check_explore_output_paths(
        wiki=Path("demo/out"), gen_tests=Path("demo/out"), scaffold=Path("demo/out")
    )  # must not raise


def test_explore_rejects_an_output_path_that_is_already_a_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from spoor.exploration import driver as driver_mod

    def _boom(*_a: object, **_k: object) -> object:
        raise AssertionError("a browser must not be launched when a path is invalid")

    monkeypatch.setattr(driver_mod, "PlaywrightDriver", _boom)
    existing_file = tmp_path / "already-a-file"
    existing_file.write_text("not a directory", encoding="utf-8")
    result = runner.invoke(
        cli.app,
        ["explore", "http://localhost:8000/", "--scaffold", str(existing_file)],
    )
    assert result.exit_code != 0
    assert "--scaffold" in _flatten_cli_error(result.output)


def test_wizard_allows_scaffold_directory_to_match_wiki(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[list[str]] = []
    monkeypatch.setattr("subprocess.run", lambda argv, **_k: calls.append(argv))
    # 1=explore, url, sandbox=n, states/requests/seconds/depth/resume/session
    # blank, wiki=demo/out, screenshots=n, gen-tests blank, scaffold=demo/out
    # (same directory as wiki -- fine now), run-now=n.
    answers = "1\nhttp://localhost:8000/\nn\n\n\n\n\n\n\ndemo/out\nn\n\ndemo/out\nn\n"
    result = runner.invoke(cli.app, ["wizard"], input=answers)
    assert result.exit_code == 0, result.output
    assert calls == []
    assert (
        "spoor explore http://localhost:8000/ --wiki demo/out --scaffold demo/out"
        in result.output
    )


# --- `spoor session` command group (ROADMAP.md §2h, closes #215) ----------


def _session_file(tmp_path: Path) -> Path:
    path = tmp_path / "captured.json"
    state = {"cookies": [{"name": "s", "value": "v", "domain": "x", "path": "/"}]}
    path.write_text(json.dumps(state), encoding="utf-8")
    return path


def test_session_add_then_list_shows_the_label(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from spoor.security import storage

    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / ".spoor-cache")
    add = runner.invoke(
        cli.app,
        [
            "session",
            "add",
            str(_session_file(tmp_path)),
            "shop.example",
            "--label",
            "customer",
        ],
    )
    assert add.exit_code == 0, add.output
    listed = runner.invoke(cli.app, ["session", "list", "shop.example"])
    assert listed.exit_code == 0, listed.output
    assert "customer" in listed.output
    # Never the stored cookie value (§2h) — the whole point of metadata-only.
    assert "s3ss10n" not in listed.output and "'v'" not in listed.output


def test_session_add_accepts_a_full_url_for_the_site(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from spoor.security import storage

    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / ".spoor-cache")
    add = runner.invoke(
        cli.app,
        [
            "session",
            "add",
            str(_session_file(tmp_path)),
            "https://shop.example/login",
            "--label",
            "customer",
        ],
    )
    assert add.exit_code == 0, add.output
    listed = runner.invoke(cli.app, ["session", "list"])
    assert "shop.example" in listed.output


def test_session_add_rejects_a_malformed_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from spoor.security import storage

    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / ".spoor-cache")
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    result = runner.invoke(
        cli.app, ["session", "add", str(bad), "shop.example", "--label", "customer"]
    )
    assert result.exit_code != 0


def test_session_remove_reports_removed_then_nothing_to_remove(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from spoor.security import storage

    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / ".spoor-cache")
    runner.invoke(
        cli.app,
        [
            "session",
            "add",
            str(_session_file(tmp_path)),
            "shop.example",
            "--label",
            "customer",
        ],
    )
    first = runner.invoke(cli.app, ["session", "remove", "shop.example", "customer"])
    assert first.exit_code == 0
    assert "Removed" in first.output
    second = runner.invoke(cli.app, ["session", "remove", "shop.example", "customer"])
    assert second.exit_code == 0
    assert "nothing removed" in second.output


def test_session_list_with_nothing_stored_says_so(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from spoor.security import storage

    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / ".spoor-cache")
    result = runner.invoke(cli.app, ["session", "list"])
    assert result.exit_code == 0
    assert "No stored sessions" in result.output


def test_gui_reports_a_launch_failure_and_exits_nonzero(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from spoor.gui import launch

    def refuse(*_args: object, **_kwargs: object) -> None:
        raise launch.GuiError("Could not listen on 127.0.0.1:1: in use")

    monkeypatch.setattr(launch, "start_gui", refuse)
    result = runner.invoke(cli.app, ["gui", "--no-browser"])
    assert result.exit_code == 1
    assert "Could not listen" in result.output


def test_gui_has_no_host_option() -> None:
    # Loopback-only is non-configurable (ROADMAP.md §2i): no --host to pass.
    result = runner.invoke(cli.app, ["gui", "--host", "0.0.0.0"])
    assert result.exit_code != 0
    assert "No such option" in result.output
