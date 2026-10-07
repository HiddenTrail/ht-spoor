"""Spoor CLI entry point (ROADMAP.md §2a).

The whole product surface on top of the resolution/extraction machinery:
`spoor run config.yaml -o output.json`. The `run` command dispatches the config
through the resolution ladder (§2), writes the chosen output format, and prints a
run summary (§2d observability); later phases add their own commands as they land.

`spoor wizard` builds any other command's argument line interactively, one prompt
at a time, and shows the exact resolved command before anything runs — for anyone
who finds hand-typing a long flag combination risky to get right. It never
duplicates a command's logic: it only assembles the argv a real invocation would
take and, if confirmed, runs that invocation as a subprocess.
"""

from __future__ import annotations

import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Annotated

import click
import typer

if TYPE_CHECKING:
    from spoor.exploration.control import RunBudget, RunController

from spoor.core import extract
from spoor.core.config import load_config
from spoor.operational.observability import RunSummary
from spoor.operational.output import resolve_format, write_records
from spoor.serving.store import (
    MapEntry,
    MapStore,
    shareable_api_surface,
    shareable_exploration_map,
)

app = typer.Typer(
    name="spoor",
    help="Give your agents a map of the web.",
    no_args_is_help=True,
    add_completion=False,
)


@app.callback()
def main() -> None:
    """Give your agents a map of the web.

    A callback (even a no-op) keeps `run` as an explicit subcommand, so the
    documented `spoor run config.yaml` interface holds instead of Typer
    collapsing a single-command app into `spoor config.yaml`.
    """


@app.command()
def run(
    config: Annotated[Path, typer.Argument(help="Path to a config file.")],
    output: Annotated[
        Path, typer.Option("-o", "--output", help="Where to write output.")
    ] = Path("output.json"),
    output_format: Annotated[
        str | None,
        typer.Option(
            "-f",
            "--format",
            help=(
                "Output format (json, jsonl, csv, md, sqlite, parquet); "
                "inferred from -o if omitted."
            ),
        ),
    ] = None,
    healing_report: Annotated[
        Path | None,
        typer.Option(
            "--healing-report",
            help=(
                "Also write a markdown report of this run's tier-3 self-healing "
                "activity to this file: for each field whose configured selector "
                "stopped matching, the old selector, the locator tier 3 "
                "re-resolved it to, its confidence, and a suggested config fix. "
                "Confident heals and uncertain matches (flagged for review, never "
                "applied automatically) are reported separately. Nothing is "
                "written when nothing healed this run."
            ),
        ),
    ] = None,
) -> None:
    """Run a config against its target and write the extracted records."""
    cfg = load_config(config.read_text(encoding="utf-8"))
    try:
        fmt = resolve_format(output, output_format)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    result = extract.run_report(cfg)
    write_records(result.records, cfg, output, fmt)
    # Remember this run in the local map so the read-only serving layer (§2f)
    # can answer for this URL later without re-crawling — the records plus the
    # §2h-safe projection of the observed API surface.
    surface = shareable_api_surface(
        api_spec=result.api_spec,
        graphql=result.graphql,
        synthesized_spec=result.synthesized_spec,
        action_correlation=result.action_correlation,
        bundle_endpoint_count=len(result.bundle_endpoints),
    )
    MapStore().record(
        cfg.target,
        result.records,
        tier=result.tier,
        api_surface=surface,
        # Kept local-only so a caller-forced recheck (§2f) can re-run this exact
        # extraction; never projected into a served response.
        config=cfg.model_dump(mode="json"),
    )
    typer.echo(f"Wrote {len(result.records)} record(s) to {output} ({fmt})")
    typer.echo(RunSummary.from_result(result).render())
    if healing_report is not None:
        from spoor.operational.healing_report import render_healing_report

        report = render_healing_report(result.heal_events)
        if report is None:
            typer.echo("  healing report:  nothing healed this run, none written")
        else:
            healing_report.write_text(report, encoding="utf-8")
            typer.echo(f"  healing report:  {healing_report}")


def _check_explore_output_paths(
    *, wiki: Path | None, gen_tests: Path | None, scaffold: Path | None
) -> None:
    """Refuse, before any browser is launched, an output flag whose path already
    exists as something other than a directory.

    `--wiki`, `--gen-tests`, and `--scaffold` all write *into* a directory, each
    under its own filename(s) that never collide with another's (a wiki's
    `index.html`, a generated suite's `test_transition_N.py`, and the scaffold's
    fixed `interactive.yaml` never clash) — so pointing several of these flags at
    the *same* directory is fine, even a natural way to keep one run's output
    together, and is not rejected here. What is still always wrong is a path that
    already exists as something else (most commonly a plain file): the flag would
    then fail trying to create a directory where a file already sits. Checked up
    front, in one place, so that failure is an immediate, clear message instead of
    a crawl that only then crashes on write.
    """
    for name, path in (
        ("--wiki", wiki),
        ("--gen-tests", gen_tests),
        ("--scaffold", scaffold),
    ):
        if path is not None and path.exists() and not path.is_dir():
            raise typer.BadParameter(
                f"{name} {path} already exists and is not a directory — {name} "
                "writes into a directory, so this path needs to be free or "
                "already be one."
            )


def _read_element_patterns_file(flag: str, path: Path) -> list[str]:
    """Read one pattern per line from `path` for --include-element/--exclude-element
    (§2e, #152 follow-up: dozens of rules shouldn't have to be typed as repeated
    flags). Blank lines and lines starting with `#` are skipped, so a rules file can
    carry its own comments. Refused up front, before any browser is launched, same
    as every other explore output/input validation here: a missing file, or a file
    that resolves to zero patterns (every line blank or a comment — almost always a
    mistake, not an intentional "match nothing"), is an immediate, clear error
    rather than a run that silently behaves as if the flag were never passed.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise typer.BadParameter(f"{flag} @{path}: could not read file: {exc}") from exc
    patterns = [
        stripped
        for line in lines
        if (stripped := line.strip()) and not stripped.startswith("#")
    ]
    if not patterns:
        raise typer.BadParameter(
            f"{flag} @{path}: file contains no patterns (every line is blank or "
            "a '#' comment)"
        )
    return patterns


def _expand_element_patterns(
    flag: str, values: list[str] | None
) -> tuple[str, ...] | None:
    """Expand --include-element/--exclude-element values into the final pattern
    tuple `ElementRules` takes.

    A value starting with `@` names a file of patterns, one per line, instead of
    being a literal pattern itself — so dozens of rules can live in a file (under
    version control, reused across runs) rather than as that many repeated flags.
    Literal and `@file` values freely mix within the same flag's repeated uses.
    """
    if not values:
        return None
    expanded: list[str] = []
    for value in values:
        if value.startswith("@"):
            expanded.extend(_read_element_patterns_file(flag, Path(value[1:])))
        else:
            expanded.append(value)
    return tuple(expanded)


class _CliProgress:
    """A dependency-free live spinner/bar for `spoor explore` (§2d observability).

    Ticked from `explorer.explore`'s opt-in `progress` callback, on the same thread
    the crawl runs on — never a second thread polling the driver, since Playwright's
    sync API is not safe to touch from any thread but the one that created it. When
    a `max_states` or `max_requests` bound is set, renders a determinate
    `[####------] NN%` gauge against it (states take priority, since that is what a
    reader usually means by "how much of the site is mapped"); unbounded, renders a
    `|/-\\` spinner instead — there is no total to show a percentage of. Either way
    the live counts (states, requests, elapsed seconds) are always shown alongside
    it. Silently does nothing when stdout isn't a real terminal (piped, redirected
    to a file, or running under a test runner), so non-interactive output is never
    polluted with carriage-return control characters, and throttled to redraw at
    most ~10 times a second so a fast crawl spends its time exploring, not
    repainting a terminal.
    """

    _FRAMES = "|/-\\"
    _MIN_INTERVAL_S = 0.1
    _WIDTH = 20

    def __init__(self, controller: RunController, budget: RunBudget) -> None:
        self._controller = controller
        self._budget = budget
        self._frame = 0
        self._last_render = 0.0
        self._active = sys.stdout.isatty()

    def tick(self) -> None:
        """Called once per state discovered and once per action fired."""
        if not self._active:
            return
        now = time.monotonic()
        if now - self._last_render < self._MIN_INTERVAL_S:
            return
        self._last_render = now
        self._render()

    def _render(self) -> None:
        self._frame += 1
        states, requests = self._controller.states, self._controller.requests
        elapsed = self._controller.elapsed()
        total = self._budget.max_states or self._budget.max_requests
        count = states if self._budget.max_states is not None else requests
        if total is not None:
            pct = min(100, int(100 * count / total))
            filled = (pct * self._WIDTH) // 100
            gauge = f"[{'#' * filled}{'-' * (self._WIDTH - filled)}] {pct:3d}%"
        else:
            gauge = self._FRAMES[self._frame % len(self._FRAMES)]
        line = f"\r{gauge} {states} state(s), {requests} request(s), {elapsed:0.0f}s"
        sys.stdout.write(line.ljust(78))
        sys.stdout.flush()

    def finish(self) -> None:
        """Clear the line so whatever prints next starts clean."""
        if not self._active:
            return
        sys.stdout.write("\r" + " " * 78 + "\r")
        sys.stdout.flush()


@app.command()
def explore(
    url: Annotated[str, typer.Argument(help="URL to start exploring from.")],
    sandbox: Annotated[
        bool,
        typer.Option(
            "--sandbox",
            help=(
                "Declare this target a sandbox so destructive actions (delete, buy, "
                "pay, ...) are exercised. Only ever use this on a local or test "
                "system you own; on any real site those actions are always skipped."
            ),
        ),
    ] = False,
    max_states: Annotated[
        int | None,
        typer.Option(help="Stop after discovering this many distinct states."),
    ] = None,
    max_requests: Annotated[
        int | None, typer.Option(help="Stop after firing this many actions.")
    ] = None,
    max_seconds: Annotated[
        float | None, typer.Option(help="Stop after this many seconds of wall-clock.")
    ] = None,
    max_depth: Annotated[
        int | None,
        typer.Option(
            help=(
                "Only map pages within this many clicks of the start. The crawl works "
                "outward layer by layer, so 1 maps the start page and everything one "
                "click away, 2 adds the next layer, and so on. Unlimited if unset."
            )
        ),
    ] = None,
    resume_from: Annotated[
        str | None,
        typer.Option(
            "--resume-from",
            help=(
                "Continue an earlier exploration of this URL instead of starting over. "
                "Give a selector naming the screen to pick up from, as it was mapped "
                "before: 'id:<prefix>' matches a screen's id (see an earlier run's map "
                "or wiki for ids). The crawl continues outward from there, and any "
                "--max-depth is counted in clicks from that screen, not the start. "
                "Newly found screens are added to the saved map. Refused if the "
                "selector names no screen or several, or if the start page has changed "
                "since the map was saved."
            ),
        ),
    ] = None,
    session: Annotated[
        Path | None,
        typer.Option(
            "--session",
            help=(
                "Explore as a logged-in user, using a session you already captured "
                "yourself (a storage-state file from Playwright's "
                "context.storage_state(), or from the same login flow the --scaffold "
                "help text points at) — or the name of one you stored earlier with "
                "`spoor session add`. Spoor never logs in on its own; this only "
                "replays a session you already have. Combines freely with "
                "--resume-from: that picks up where a crawl continues from, this "
                "decides whether it's authenticated, and neither depends on the "
                "other."
            ),
        ),
    ] = None,
    wiki: Annotated[
        Path | None,
        typer.Option(
            "--wiki",
            help=(
                "Also write a browsable wiki of the map (one HTML page per state and "
                "transition, plus an overview) into this directory. Open its "
                "index.html in a browser."
            ),
        ),
    ] = None,
    gen_tests: Annotated[
        Path | None,
        typer.Option(
            "--gen-tests",
            help=(
                "Also write a runnable pytest regression suite of the map into this "
                "directory: one test per mapped transition that replays to it, fires "
                "the action, and asserts what it changed. Re-run the suite later "
                "against the live site to catch drift. Running it needs Playwright "
                "installed; captured secrets are redacted before they reach a test."
            ),
        ),
    ] = None,
    assert_no_new_signals: Annotated[
        bool,
        typer.Option(
            "--assert-no-new-signals",
            help=(
                "Requires --gen-tests. Adds a reverse check to every generated test: "
                "besides asserting the console/storage/network values recorded during "
                "this crawl still appear, also assert nothing *beyond* them appears — "
                "so a later change that starts firing an unexpected extra request or "
                "logging a new console line fails the suite instead of passing it "
                "silently. Checked only for a signal kind that had at least one value "
                "recorded; a kind with none recorded is left unchecked, since ordinary "
                "page-load noise is never recorded either and would make an 'assert "
                "nothing at all' check fail on its own. No value normalization yet, so "
                "a value that legitimately varies run to run (a timestamp, a random "
                "request id) can make this check noisier than the default suite."
            ),
        ),
    ] = False,
    scaffold: Annotated[
        Path | None,
        typer.Option(
            "--scaffold",
            help=(
                "Also write a config-scaffold YAML file (interactive.yaml) into "
                "this directory, listing what a future, not-yet-built interactive "
                "round would need: discovered fields with a best-guess value type, "
                "discovered login points (flagged only — Spoor never automates a "
                "login, point session: at a storage-state file you already "
                "exported), and discovered actions skipped for being destructive. "
                "Filling it in does nothing on its own today."
            ),
        ),
    ] = None,
    include_elements: Annotated[
        list[str] | None,
        typer.Option(
            "--include-element",
            help=(
                "Only attempt an actionable element whose visible label matches one "
                "of these patterns (e.g. 'Add to cart*'; '*' and '?' wildcards, "
                "case-sensitive). Repeatable. A value starting with '@' names a file "
                "of patterns instead (one per line, blank lines and '#' comments "
                "skipped) — handy once there are more than a few, and reusable "
                "across runs: --include-element @rules.txt. Unset: every discovered "
                "element is a candidate, same as without this option. An "
                "--exclude-element match always wins over this. Narrows what's "
                "attempted only — destructive actions (delete, buy, pay, ...) still "
                "only ever fire in a sandbox, regardless of what this matches."
            ),
        ),
    ] = None,
    exclude_elements: Annotated[
        list[str] | None,
        typer.Option(
            "--exclude-element",
            help=(
                "Never attempt an actionable element whose visible label matches one "
                "of these patterns (e.g. '*Logout*'; '*' and '?' wildcards, "
                "case-sensitive). Repeatable, and a value starting with '@' names a "
                "file of patterns instead — see --include-element. Wins over "
                "--include-element when both match the same element."
            ),
        ),
    ] = None,
    screenshots: Annotated[
        bool,
        typer.Option(
            "--screenshots",
            help=(
                "Include screenshots in the wiki (requires --wiki): a full-page "
                "picture of each screen, a clip of each interactive element, and a "
                "picture of what a dropdown or list reveals when opened. Off by "
                "default: screenshots are not captured unless you ask for them, "
                "because a picture can show secrets (a token or personal data on the "
                "page) that cannot be automatically blanked out the way text can. Only "
                "turn this on when you are comfortable sharing the images."
            ),
        ),
    ] = False,
) -> None:
    """Explore a target with no config, mapping its state-action graph.

    Points a headless browser at the URL, discovers the actionable elements on each
    screen, fires each one, and records where it leads — building a graph of what
    happens when you press every button. Destructive actions are only ever performed
    against a sandbox you declare with --sandbox; on any other site they are always
    skipped and never fired. An element that can't actually be clicked (gone, hidden,
    or covered by the time it's reached) is recorded as skipped and the run continues.
    Bound the run with the budget options, and press Ctrl-C to stop it early at any
    time. Pass --resume-from to continue an earlier exploration of this URL from a
    named screen instead of starting over: the crawl picks up there, any --max-depth is
    counted from that screen, and the newly found screens are merged into the saved map.
    Pass --session to explore as a logged-in user, using a session you captured
    yourself, or one you stored earlier under a name with `spoor session add` —
    Spoor never logs in on its own, so anything behind a login stays unmapped
    without one. Pass --wiki to also write a browsable wiki of the
    result, and --screenshots to include pictures in that wiki — a full-page
    shot of each screen, a clip of each interactive element, and a shot of what
    a dropdown or list reveals when opened (off by default, because a picture
    can't have secrets blanked out the way captured text can). Pass --gen-tests
    to also write a runnable
    pytest regression suite of the map (one test per mapped transition) you can re-run
    against the live site later to catch drift. Add --assert-no-new-signals to also
    make each generated test fail if the live replay produces a console message,
    storage key, or network request that wasn't seen anywhere during this crawl — not
    just check that what was recorded is still there, but that nothing unexpected was
    added since. Pass --scaffold to also write a
    config-scaffold YAML file (interactive.yaml) into a directory, naming discovered
    fields, login points, and destructive actions — a starting point for a planned,
    not-yet-built interactive round; filling it in does nothing on its own yet. The
    mapped graph is also saved to the local map, so `spoor serve`/`serve-mcp` can hand
    it back later without re-exploring. Pass --include-element and/or
    --exclude-element to scope which elements are attempted at all, by label pattern
    (or @<file> for a file of patterns, one per line) — this only narrows what's
    attempted, never what's permitted: a destructive action still only ever fires in
    a sandbox either way.
    """
    import signal

    from spoor.exploration.control import RunBudget, RunController
    from spoor.exploration.driver import PlaywrightDriver
    from spoor.exploration.element_rules import ElementRules
    from spoor.exploration.explorer import ElementShot
    from spoor.exploration.explorer import explore as explore_target
    from spoor.exploration.resume import ResumeError, resume_exploration
    from spoor.exploration.screenshot_store import ImageRef

    if screenshots and wiki is None:
        raise typer.BadParameter(
            "--screenshots needs --wiki: there is no wiki to put "
            "the images in without it."
        )
    if assert_no_new_signals and gen_tests is None:
        raise typer.BadParameter(
            "--assert-no-new-signals needs --gen-tests: there is no generated "
            "suite to add the check to without it."
        )
    _check_explore_output_paths(wiki=wiki, gen_tests=gen_tests, scaffold=scaffold)
    if session is not None:
        from urllib.parse import urlsplit

        from spoor.security.session import SessionError, load_session

        try:
            load_session(session, domain=urlsplit(url).netloc)
        except SessionError as exc:
            raise typer.BadParameter(str(exc)) from exc
    # The saved map to continue, when resuming: the §2h-shareable projection an earlier
    # explore of this exact URL stored (§2f). Loaded up front so a missing map fails
    # before a browser is launched.
    saved_map: dict[str, object] | None = None
    if resume_from is not None:
        entry = MapStore().get(url)
        if entry is None or entry.exploration is None:
            raise typer.BadParameter(
                f"there is no saved exploration map for {url} to resume from — run "
                "`spoor explore <url>` first to map it, then resume."
            )
        saved_map = entry.exploration
    try:
        budget = RunBudget(
            max_states=max_states,
            max_requests=max_requests,
            max_seconds=max_seconds,
            max_depth=max_depth,
        )
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc
    controller = RunController(budget)
    element_rules = ElementRules(
        include=_expand_element_patterns("--include-element", include_elements),
        exclude=_expand_element_patterns("--exclude-element", exclude_elements),
    )
    cli_progress = _CliProgress(controller, budget)
    # The opt-in screenshot sinks: dicts only when asked for, so a default run captures
    # no pixels at all (§2e slice 8). During exploration each image is written straight
    # to disk under the wiki directory as it is captured (§2e slice 8f) — and only when
    # the picture is new, since a deduplicating store reuses a file already written for
    # an identical or near-identical screen (§2e slice 8g). The sinks hold only
    # references, so a run never piles image bytes in memory. The wiki writer then
    # embeds those references: one full-page shot per screen (8b), one clip per element
    # (8d) — a clip that is a region of its page embeds as a crop of that shared picture
    # rather than a file of its own (§2e slice 8g). All behind this single opt-in.
    # `--screenshots` requires `--wiki` (validated above), so the output directory is
    # known up front and is where both the images and the pages that embed them land.
    shots: dict[str, ImageRef] | None = {} if screenshots else None
    element_shots: dict[str, list[ElementShot]] | None = {} if screenshots else None
    screenshot_dir: Path | None = wiki if screenshots else None
    # Ctrl-C throws the kill switch, so the run stops gracefully at the next action
    # rather than aborting mid-click. Restore the previous handler afterwards so the
    # run doesn't leave a global side effect behind.
    previous_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, lambda *_: controller.kill())
    try:
        with PlaywrightDriver(
            url, session=str(session) if session is not None else None
        ) as driver:
            if saved_map is not None:
                assert resume_from is not None  # saved_map is set only when resuming
                try:
                    graph = resume_exploration(
                        driver,
                        target=url,
                        controller=controller,
                        saved_map=saved_map,
                        selector=resume_from,
                        declared_sandbox=sandbox,
                        element_rules=element_rules,
                        screenshots=shots,
                        element_screenshots=element_shots,
                        screenshot_dir=screenshot_dir,
                        progress=cli_progress.tick,
                    )
                except (ResumeError, ValueError) as exc:
                    raise typer.BadParameter(str(exc)) from exc
            else:
                graph = explore_target(
                    driver,
                    target=url,
                    controller=controller,
                    declared_sandbox=sandbox,
                    element_rules=element_rules,
                    screenshots=shots,
                    element_screenshots=element_shots,
                    screenshot_dir=screenshot_dir,
                    progress=cli_progress.tick,
                )
    finally:
        cli_progress.finish()
        signal.signal(signal.SIGINT, previous_handler)

    # Remember this exploration in the local map so the read-only serving layer
    # (§2f) can answer "what happens when I click X" for this URL later without
    # re-exploring — the §2h-safe projection of the state-action graph. No extracted
    # records for an explore run, so records is empty and there is no tier.
    MapStore().record(
        url,
        [],
        exploration=shareable_exploration_map(graph),
    )

    typer.echo(f"{'Resumed' if saved_map is not None else 'Explored'} {url}")
    if session is not None:
        typer.echo("  session:           supplied — explored as a logged-in user")
    typer.echo(f"  states discovered: {len(graph.states)}")
    typer.echo(f"  transitions:       {len(graph.transitions)}")
    typer.echo(f"  actions skipped:   {len(graph.skipped)}")
    if graph.skipped:
        from spoor.exploration.safety import DESTRUCTIVE_SKIP_REASON

        # An action can be skipped for two unrelated reasons, and only one of them
        # is about the sandbox gate — check each skip's own reason (the safety
        # module names DESTRUCTIVE_SKIP_REASON for exactly this, so a skip isn't
        # misreported as destructive when it wasn't) rather than assuming every
        # skip here came from the gate.
        destructive = sum(
            1 for skip in graph.skipped if skip.reason == DESTRUCTIVE_SKIP_REASON
        )
        other = len(graph.skipped) - destructive
        if destructive and not sandbox:
            typer.echo(
                f"  ({destructive} destructive, skipped — this target is not a "
                "declared sandbox)"
            )
        if other:
            typer.echo(
                f"  ({other} could not be reached or performed after replay)"
            )

    if gen_tests is not None:
        from spoor.testgen import render_suite

        written = render_suite(
            graph,
            gen_tests,
            target=url,
            assert_no_new_signals=assert_no_new_signals,
        )
        # One test file per transition plus the two fixed support modules, so the count
        # of runnable regression tests is the written total minus those two (0 when the
        # graph had no transitions and nothing was written at all).
        test_count = max(len(written) - 2, 0)
        typer.echo(f"  tests written to:  {gen_tests} ({test_count} test(s))")

    if scaffold is not None:
        from spoor.scaffold.interactive_config import render_scaffold

        written_scaffold = render_scaffold(graph, scaffold, target=url)
        if written_scaffold is not None:
            typer.echo(f"  scaffold written to: {written_scaffold}")

    if wiki is not None:
        from spoor.exploration.wiki import render_wiki

        render_wiki(
            graph,
            wiki,
            target=url,
            screenshots=shots,
            element_screenshots=element_shots,
        )
        typer.echo(f"  wiki written to:   {wiki / 'index.html'}")
        if screenshots:
            all_shots = [s for shots_ in (element_shots or {}).values() for s in shots_]
            element_count = sum(1 for s in all_shots if s.clip)
            opened_count = sum(1 for s in all_shots if s.opened)
            # How many distinct image files back all those references: dedup means many
            # screens/clips can share one file, and a contained clip is a crop of a
            # picture already counted, so the file total is typically far below the
            # reference total (§2e slice 8g).
            all_refs = [*(shots or {}).values()]
            all_refs += [s.clip for s in all_shots if s.clip is not None]
            all_refs += [s.opened for s in all_shots if s.opened is not None]
            file_count = len({ref.src for ref in all_refs})
            typer.echo(f"  screenshots:       {len(shots or {})} screens embedded")
            typer.echo(f"  element clips:     {element_count} embedded")
            typer.echo(f"  opened contents:   {opened_count} embedded")
            typer.echo(f"  image files:       {file_count} written after dedup")


@app.command()
def serve(
    host: Annotated[
        str, typer.Option(help="Address to bind the read-only API server to.")
    ] = "127.0.0.1",
    port: Annotated[int, typer.Option(help="Port to serve on.")] = 8000,
    recheck: Annotated[
        bool,
        typer.Option(
            "--recheck",
            help=(
                "Also allow forcing a re-check of a mapped URL (re-runs its "
                "extraction and refreshes the map). Off by default."
            ),
        ),
    ] = False,
) -> None:
    """Serve the captured map over a read-only REST API (ROADMAP.md §2f).

    Answers questions about what earlier runs mapped; it never changes a target.
    By default every route only reads the stored map. With --recheck it also
    accepts a request to re-check a mapped URL: that re-runs the URL's extraction
    (a fresh read of the site, never a change to it) and refreshes the map.
    Requires the optional serving extras: pip install 'ht-spoor[serve]'.
    """
    try:
        import uvicorn
    except ModuleNotFoundError as exc:  # pragma: no cover - exercised via message
        raise typer.BadParameter(
            "The serving extras are not installed. Run: pip install 'ht-spoor[serve]'"
        ) from exc
    from spoor.serving.api import create_app

    store = MapStore()
    recheck_fn = _build_recheck(store) if recheck else None
    uvicorn.run(  # pragma: no cover
        create_app(store, recheck=recheck_fn), host=host, port=port
    )


@app.command(name="serve-mcp")
def serve_mcp(
    recheck: Annotated[
        bool,
        typer.Option(
            "--recheck",
            help=(
                "Also expose a tool to force a re-check of a mapped URL (re-runs "
                "its extraction and refreshes the map). Off by default."
            ),
        ),
    ] = False,
) -> None:
    """Serve the captured map to agents over a read-only MCP server (stdio).

    The same answers as `spoor serve`, exposed as MCP tools for an agent to
    consult; it never changes a target. With --recheck it also exposes a tool to
    re-check a mapped URL (re-runs the URL's extraction and refreshes the map — a
    fresh read of the site, never a change to it). Requires the optional serving
    extras: pip install 'ht-spoor[serve]'.
    """
    try:
        from spoor.serving.mcp_server import create_mcp_server
    except ModuleNotFoundError as exc:  # pragma: no cover - exercised via message
        raise typer.BadParameter(
            "The serving extras are not installed. Run: pip install 'ht-spoor[serve]'"
        ) from exc
    import asyncio

    store = MapStore()
    recheck_fn = _build_recheck(store) if recheck else None
    server = create_mcp_server(store, recheck=recheck_fn)
    asyncio.run(server.run_stdio_async())  # pragma: no cover


session_app = typer.Typer(
    name="session",
    help="Store and manage named, reusable logged-in sessions, per site.",
    no_args_is_help=True,
    add_completion=False,
)
app.add_typer(session_app, name="session")


@session_app.command(name="add")
def session_add(
    file: Annotated[
        Path, typer.Argument(help="A storage-state file you already captured.")
    ],
    site: Annotated[
        str,
        typer.Argument(
            help="The site this session is for — a bare domain or a full URL."
        ),
    ],
    label: Annotated[
        str, typer.Option("--label", help="The name to store this session under.")
    ],
) -> None:
    """Store a captured session under a name, scoped to a site.

    Validates the file is a real storage-state export before storing it, the
    same check `--session <file>` already applies. Re-adding an existing label
    for the same site replaces what it points to — useful once a session
    expires and you've captured a fresh one under the same name.
    """
    from spoor.security.session import SessionError, load_session
    from spoor.security.session_store import SessionStore, domain_of

    try:
        loaded = load_session(file)
    except SessionError as exc:
        raise typer.BadParameter(str(exc)) from exc
    domain = domain_of(site)
    SessionStore().add(domain, label, loaded.raw)
    typer.echo(f"Stored session {label!r} for {domain}.")


@session_app.command(name="list")
def session_list(
    site: Annotated[
        str | None,
        typer.Argument(
            help="Only list sessions for this site. Every stored session if omitted."
        ),
    ] = None,
) -> None:
    """List stored sessions — labels and timestamps only, never their contents.

    A stored session's cookies/storage values are never shown or exported by
    this command (ROADMAP.md §2h) — only what you'd need to decide which to use
    or remove.
    """
    from spoor.security.session_store import SessionStore, domain_of

    domain = domain_of(site) if site is not None else None
    sessions = SessionStore().list(domain)
    if not sessions:
        if domain is None:
            typer.echo("No stored sessions.")
        else:
            typer.echo(f"No stored sessions for {domain}.")
        return
    for meta in sessions:
        used = meta.last_used_at or "never"
        typer.echo(
            f"{meta.domain}  {meta.label!r}  "
            f"created {meta.created_at}  last used {used}"
        )


@session_app.command(name="remove")
def session_remove(
    site: Annotated[str, typer.Argument(help="The site the session is stored for.")],
    label: Annotated[str, typer.Argument(help="The stored session's name.")],
) -> None:
    """Delete a stored session."""
    from spoor.security.session_store import SessionStore, domain_of

    domain = domain_of(site)
    removed = SessionStore().remove(domain, label)
    if removed:
        typer.echo(f"Removed session {label!r} for {domain}.")
    else:
        typer.echo(f"No stored session {label!r} for {domain} — nothing removed.")


@app.command(name="apply-scaffold")
def apply_scaffold_cmd(
    url: Annotated[
        str, typer.Argument(help="A URL already mapped by `spoor explore`.")
    ],
    scaffold: Annotated[
        Path,
        typer.Argument(
            help=(
                "A scaffold YAML file — interactive.yaml inside the directory "
                "--scaffold wrote."
            )
        ),
    ],
    sandbox: Annotated[
        bool,
        typer.Option(
            "--sandbox",
            help=(
                "Declare this target a sandbox. Only ever use this on a local or "
                "test system you own — on any real site, typing is always skipped."
            ),
        ),
    ] = False,
    session: Annotated[
        Path | None,
        typer.Option(
            "--session",
            help=(
                "Apply the scaffold as a logged-in user, using a session you already "
                "captured yourself — or the name of one stored earlier with `spoor "
                "session add`. Only needed if the screen the scaffold's fields live "
                "on is itself behind a login; Spoor never logs in on its own."
            ),
        ),
    ] = None,
    wiki: Annotated[
        Path | None,
        typer.Option(
            "--wiki",
            help=(
                "Also refresh the wiki at this directory (the same one --wiki wrote) "
                "so it shows what a filled-in field revealed. Only rewritten when a "
                "fill actually changed the page — states/transitions it added are "
                "clearly marked as reached via this config, not a click."
            ),
        ),
    ] = None,
) -> None:
    """Type a filled-in interactive-round scaffold's values into their fields.

    Reads a URL's saved exploration map and a scaffold file you've filled in (from
    `spoor explore --scaffold <dir>`, at `<dir>/interactive.yaml`) and types each
    field's pinned value into it — only for fields on the screen the crawl started
    from. That is the whole of what
    this does: it never presses Enter, never clicks a submit control, and never fires
    any action beyond typing. Applying or submitting a value is a separate,
    not-yet-built capability (see ROADMAP.md §2e) — this command only gets a value
    into a field, honestly, so you can see it land.

    Only runs against a target you declare a sandbox with --sandbox (a loopback
    address such as localhost, or this flag) — on any other site nothing is typed,
    the same rule exploration's own destructive-action gate already follows.
    Pass --session if the scaffold's fields live behind a login, using a session
    you already captured yourself or one stored earlier with `spoor session add`;
    Spoor never logs in on its own.

    When a fill changes what's on the page, that new state is read the same
    read-only way exploration reads any other state, and saved into the map
    alongside what the original crawl found — never overwriting it, only adding to
    it. Pass --wiki to see it there too, clearly marked as reached by typing rather
    than a click.
    """
    entry = MapStore().get(url)
    if entry is None or entry.exploration is None:
        raise typer.BadParameter(
            f"there is no saved exploration map for {url} — run `spoor explore "
            "<url>` first to map it."
        )
    from spoor.exploration.driver import PlaywrightDriver
    from spoor.exploration.persisted_map import load_exploration_map
    from spoor.scaffold.apply import apply_scaffold, load_scaffold

    if session is not None:
        from urllib.parse import urlsplit

        from spoor.security.session import SessionError, load_session

        try:
            load_session(session, domain=urlsplit(url).netloc)
        except SessionError as exc:
            raise typer.BadParameter(str(exc)) from exc

    graph = load_exploration_map(entry.exploration)
    scaffold_data = load_scaffold(scaffold)
    states_before, transitions_before = len(graph.states), len(graph.transitions)
    with PlaywrightDriver(
        url, session=str(session) if session is not None else None
    ) as driver:
        applied, failed = apply_scaffold(
            driver, graph, scaffold_data, target=url, declared_sandbox=sandbox
        )
    typer.echo(f"Applied {len(applied)} field(s):")
    for applied_field in applied:
        typer.echo(f"  state {applied_field.state}: {applied_field.name!r}")
    if failed:
        typer.echo(f"Could not apply {len(failed)} field(s):")
        for failed_field in failed:
            typer.echo(
                f"  state {failed_field.state}: {failed_field.name!r} — "
                f"{failed_field.reason}"
            )
    typer.echo("Nothing was submitted or clicked beyond typing.")

    new_states = len(graph.states) - states_before
    new_transitions = len(graph.transitions) - transitions_before
    if new_states or new_transitions:
        MapStore().record(
            url,
            entry.records,
            tier=entry.tier,
            api_surface=entry.api_surface,
            config=entry.config,
            exploration=shareable_exploration_map(graph),
        )
        typer.echo(
            f"  map updated: +{new_states} state(s), +{new_transitions} "
            "transition(s) revealed by this config"
        )
        if wiki is not None:
            from spoor.exploration.wiki import render_wiki

            render_wiki(graph, wiki, target=url)
            typer.echo(f"  wiki refreshed at: {wiki / 'index.html'}")


def _wizard_optional_str(question: str) -> str | None:
    """Prompt for an optional value; blank means "not given"."""
    raw = typer.prompt(f"{question} (blank to skip)", default="", show_default=False)
    return raw.strip() or None


def _wizard_optional_int(question: str) -> int | None:
    """Prompt for an optional whole number, re-asking on anything unparsable."""
    while True:
        raw = typer.prompt(
            f"{question} (blank to skip)", default="", show_default=False
        )
        if not raw.strip():
            return None
        try:
            return int(raw)
        except ValueError:
            typer.echo(f"  {raw!r} isn't a whole number — try again.")


def _wizard_optional_float(question: str) -> float | None:
    """Prompt for an optional number, re-asking on anything unparsable."""
    while True:
        raw = typer.prompt(
            f"{question} (blank to skip)", default="", show_default=False
        )
        if not raw.strip():
            return None
        try:
            return float(raw)
        except ValueError:
            typer.echo(f"  {raw!r} isn't a number — try again.")


def _wizard_choose_command() -> str:
    """Ask which command to build, by number, defaulting to the most common one."""
    options = {
        "1": "explore",
        "2": "apply-scaffold",
        "3": "run",
        "4": "serve",
        "5": "serve-mcp",
    }
    typer.echo("Which Spoor command do you want to build?")
    for key, name in options.items():
        typer.echo(f"  {key}) {name}")
    choice = typer.prompt(
        "Choice",
        type=click.Choice(list(options)),
        default="1",
        show_choices=False,
    )
    return options[choice]


def _wizard_explore_args() -> list[str]:
    url = typer.prompt("URL to explore")
    args = ["explore", url]
    if typer.confirm(
        "Declare this target a sandbox? (destructive actions will fire)",
        default=False,
    ):
        args.append("--sandbox")
    max_states = _wizard_optional_int("Max states")
    if max_states is not None:
        args += ["--max-states", str(max_states)]
    max_requests = _wizard_optional_int("Max requests")
    if max_requests is not None:
        args += ["--max-requests", str(max_requests)]
    max_seconds = _wizard_optional_float("Max seconds")
    if max_seconds is not None:
        args += ["--max-seconds", str(max_seconds)]
    max_depth = _wizard_optional_int("Max depth (clicks from the start page)")
    if max_depth is not None:
        args += ["--max-depth", str(max_depth)]
    resume_from = _wizard_optional_str("Resume from a selector (e.g. id:abc123)")
    if resume_from is not None:
        args += ["--resume-from", resume_from]
    session = _wizard_optional_str(
        "Explore as a logged-in user, using a captured session file at"
    )
    if session is not None:
        args += ["--session", session]
    wiki = _wizard_optional_str("Write a wiki to this directory")
    if wiki is not None:
        args += ["--wiki", wiki]
        if typer.confirm("Include screenshots in the wiki?", default=False):
            args.append("--screenshots")
    gen_tests = _wizard_optional_str("Write a generated test suite to this directory")
    if gen_tests is not None:
        args += ["--gen-tests", gen_tests]
    scaffold = _wizard_optional_str(
        "Write a config scaffold (interactive.yaml) into this directory"
    )
    if scaffold is not None:
        args += ["--scaffold", scaffold]
    return args


def _wizard_apply_scaffold_args() -> list[str]:
    url = typer.prompt("URL already mapped by `spoor explore`")
    scaffold = typer.prompt(
        "Scaffold YAML file (interactive.yaml inside the directory --scaffold wrote)"
    )
    args = ["apply-scaffold", url, scaffold]
    if typer.confirm(
        "Declare this target a sandbox? (required for anything to be typed)",
        default=False,
    ):
        args.append("--sandbox")
    session = _wizard_optional_str(
        "Apply as a logged-in user, using a captured session file at"
    )
    if session is not None:
        args += ["--session", session]
    wiki = _wizard_optional_str(
        "Refresh a wiki at this directory (the one --wiki wrote earlier)"
    )
    if wiki is not None:
        args += ["--wiki", wiki]
    return args


def _wizard_run_args() -> list[str]:
    config = typer.prompt("Config file")
    output = typer.prompt("Output path", default="output.json")
    args = ["run", config, "-o", output]
    fmt = _wizard_optional_str(
        "Output format (json/jsonl/csv/md/sqlite/parquet; blank infers from -o)"
    )
    if fmt is not None:
        args += ["-f", fmt]
    return args


def _wizard_serve_args() -> list[str]:
    host = typer.prompt("Host to bind to", default="127.0.0.1")
    port = typer.prompt("Port", default=8000, type=int)
    args = ["serve", "--host", host, "--port", str(port)]
    if typer.confirm("Allow forcing a re-check of a mapped URL?", default=False):
        args.append("--recheck")
    return args


def _wizard_serve_mcp_args() -> list[str]:
    args = ["serve-mcp"]
    if typer.confirm("Allow forcing a re-check of a mapped URL?", default=False):
        args.append("--recheck")
    return args


_WIZARD_BUILDERS: dict[str, Callable[[], list[str]]] = {
    "explore": _wizard_explore_args,
    "apply-scaffold": _wizard_apply_scaffold_args,
    "run": _wizard_run_args,
    "serve": _wizard_serve_args,
    "serve-mcp": _wizard_serve_mcp_args,
}


@app.command()
def wizard() -> None:
    """Build a Spoor command interactively, one prompt at a time.

    Walks you through picking a command and its flags — so you never have to
    remember which flag goes with which command, or mix one command's flags up
    with another's — then shows you the exact resolved command line before
    anything runs. Nothing is fetched, typed, launched, or written until you
    explicitly confirm running it; answering "no" just leaves you the command
    line to copy and run yourself, or adjust first.

    This never reimplements a command's own logic — it only assembles the same
    argument line `--help` documents and, if you confirm, runs that exact
    invocation as a subprocess, so it can never drift from what the real
    command actually does.
    """
    import shlex
    import subprocess
    import sys

    command = _wizard_choose_command()
    args = _WIZARD_BUILDERS[command]()

    typer.echo("")
    typer.echo("Resolved command:")
    typer.echo(f"  spoor {shlex.join(args)}")
    typer.echo("")
    if typer.confirm("Run it now?", default=False):
        subprocess.run([sys.executable, "-m", "spoor.cli", *args])
    else:
        typer.echo("Not run — copy the line above to run it yourself.")


def _build_recheck(store: MapStore) -> Callable[[str], MapEntry | None]:
    """Bind the force-recheck seam to a store (lazy import keeps core light)."""
    from spoor.serving.recheck import recheck_url

    def recheck(url: str) -> MapEntry | None:
        return recheck_url(store, url)

    return recheck


if __name__ == "__main__":  # pragma: no cover
    app()
