"""Step definitions for features/gui_jobs.feature (ROADMAP.md §2i, slice gui-2).

The GUI's run forms build a real `spoor` argument list and hand it to a job
manager that supervises the child process. Here the manager gets a FAKE runner:
it records what it was asked to start (arguments and environment) and plays a
scripted process — printing lines, writing a wiki, waiting for its stop file, or
waiting to be killed — so argument building, live logs, Stop and output links
are pinned without launching Spoor. The `@browser` scenario swaps in the real
runner and explores a local static fixture end to end.
"""

from __future__ import annotations

import os
import queue
import shlex
import threading
import time
from collections.abc import Callable, Iterator, Mapping, Sequence
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenarios, then, when

from spoor.gui.app import create_app, token_cookie
from spoor.gui.jobs import Job, JobManager
from spoor.gui.launch import start_gui
from spoor.security import storage
from spoor.serving.store import MapStore

scenarios("gui_jobs.feature")

_TOKEN = "known-test-token"
_PORT = 8766
_BASE = f"http://127.0.0.1:{_PORT}"
_FINISH_TIMEOUT_S = 10.0


# --- The fake runner -----------------------------------------------------------


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
        line = self._lines.get(timeout=_FINISH_TIMEOUT_S)
        return "" if line is None else line

    def wait(self) -> int:
        self._done.wait(_FINISH_TIMEOUT_S)
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


def _flag_value(args: Sequence[str], flag: str) -> str:
    return args[args.index(flag) + 1]


# --- Fixtures ------------------------------------------------------------------


@pytest.fixture
def context() -> Iterator[dict[str, Any]]:
    ctx: dict[str, Any] = {}
    yield ctx
    if "browser" in ctx:
        pw, browser = ctx["browser"]
        browser.close()
        pw.stop()
    if "gui" in ctx:
        ctx["gui"].stop()


@pytest.fixture
def workdir(tmp_path: Path) -> Path:
    path = tmp_path / "work"
    path.mkdir()
    return path


@pytest.fixture(autouse=True)
def temp_cache_root(workdir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The local cache under the jobs' workdir, where a real child would put it."""
    monkeypatch.setattr(storage, "CACHE_ROOT", workdir / ".spoor-cache")


def _client(context: dict[str, Any]) -> TestClient:
    client = TestClient(context["app"], base_url=_BASE, follow_redirects=False)
    client.cookies.set(token_cookie(_PORT), _TOKEN)
    return client


def _post(context: dict[str, Any], path: str, data: dict[str, str]) -> Any:
    return _client(context).post(path, data=data, headers={"origin": _BASE})


def _abs(workdir: Path, rel: str) -> str:
    return os.path.abspath(workdir / rel)


def _expected_args(workdir: Path, command: str) -> list[str]:
    out = []
    for token in shlex.split(command):
        if token.startswith("<abs:") and token.endswith(">"):
            token = _abs(workdir, token[5:-1])
        out.append(token)
    return out


def _form(datatable: list[list[str]]) -> dict[str, str]:
    _, *rows = datatable
    return {name: value.replace("\\n", "\n") for name, value in rows}


def _job(context: dict[str, Any]) -> Job:
    job = context["jobs"].get(context["job_id"])
    assert job is not None
    return job


# --- Given ---------------------------------------------------------------------


@given("the GUI app is running jobs with a fake runner")
def gui_with_fake_runner(context: dict[str, Any], workdir: Path) -> None:
    runner = FakeRunner()
    opened: list[Path] = []
    jobs = JobManager(runner, workdir)
    context.update(runner=runner, jobs=jobs, opened=opened, workdir=workdir)
    context["store"] = MapStore()
    context["app"] = create_app(
        context["store"], token=_TOKEN, port=_PORT, jobs=jobs, opener=opened.append
    )


@given(parsers.parse('the fake command will print "{line}" and exit {code:d}'))
def fake_prints(context: dict[str, Any], line: str, code: int) -> None:
    def script(proc: FakeProcess, args: Sequence[str], env: Any) -> None:
        proc.emit(line)
        proc.exit(code)

    context["runner"].script = script


@given("the fake command will write a wiki and exit 0")
def fake_writes_wiki(context: dict[str, Any]) -> None:
    def script(proc: FakeProcess, args: Sequence[str], env: Any) -> None:
        wiki = Path(_flag_value(args, "--wiki"))
        wiki.mkdir(parents=True)
        (wiki / "index.html").write_text("<h1>Wiki index</h1>", encoding="utf-8")
        # Something just outside the wiki that must never be served from it.
        (wiki.parent / "secret.txt").write_text("outside", encoding="utf-8")
        # A real explore records its map; do the same so the map link appears.
        MapStore().record(args[1], [])
        proc.emit(f"  wiki written to:   {wiki / 'index.html'}")
        proc.exit(0)

    context["runner"].script = script


@given("the fake command keeps running until its stop file appears, then exits 0")
def fake_waits_for_stop_file(context: dict[str, Any]) -> None:
    def script(proc: FakeProcess, args: Sequence[str], env: Mapping[str, str]) -> None:
        stop_file = Path(env["SPOOR_STOP_FILE"])
        deadline = time.monotonic() + _FINISH_TIMEOUT_S
        while not stop_file.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        proc.emit("Stop requested: finishing the current action, then saving.")
        proc.exit(0)

    context["runner"].script = script


@given("the fake command keeps running until it is killed")
def fake_waits_for_kill(context: dict[str, Any]) -> None:
    def script(proc: FakeProcess, args: Sequence[str], env: Any) -> None:
        proc.killed.wait(_FINISH_TIMEOUT_S)
        proc.exit(1)

    context["runner"].script = script


@given(parsers.parse('a map store that has mapped "{url}"'))
def mapped_store(context: dict[str, Any], url: str) -> None:
    context["store"].record(
        url, [{"title": "Blue mug"}], captured_at=datetime.now(UTC) - timedelta(hours=1)
    )


@given("the GUI is running on loopback with the real command runner")
def real_gui(context: dict[str, Any], workdir: Path) -> None:
    context["workdir"] = workdir
    context["gui"] = start_gui(MapStore(), workdir=workdir)


@given("a local static site is being served")
def static_site(context: dict[str, Any], live_server: str) -> None:
    context["site_url"] = f"{live_server}/explore_home.html"


# --- When ----------------------------------------------------------------------


def _submit(context: dict[str, Any], kind: str, form: dict[str, str]) -> None:
    response = _post(context, f"/new/{kind}", form)
    context["response"] = response
    if response.status_code == 303:
        context["job_id"] = response.headers["location"].rsplit("/", 1)[1]


@when("I submit the explore form with:")
def submit_explore(context: dict[str, Any], datatable: list[list[str]]) -> None:
    _submit(context, "explore", _form(datatable))


@when("I submit the run form with:")
def submit_run(context: dict[str, Any], datatable: list[list[str]]) -> None:
    _submit(context, "run", _form(datatable))


@when("I submit the apply-scaffold form with:")
def submit_apply(context: dict[str, Any], datatable: list[list[str]]) -> None:
    _submit(context, "apply-scaffold", _form(datatable))


@when("I preview the explore form with:")
def preview_explore(context: dict[str, Any], datatable: list[list[str]]) -> None:
    context["response"] = _post(context, "/preview/explore", _form(datatable))


@when(parsers.parse('I start an explore job for "{url}"'))
def start_explore(context: dict[str, Any], url: str) -> None:
    _submit(context, "explore", {"url": url})
    assert context["response"].status_code == 303


@when(parsers.parse('I start an explore job for "{url}" with a wiki folder'))
def start_explore_with_wiki(context: dict[str, Any], url: str) -> None:
    _submit(context, "explore", {"url": url, "wiki": "on", "wiki_dir": "out/wiki"})
    assert context["response"].status_code == 303


@when(parsers.parse('I start a run job for "{config}"'))
def start_run(context: dict[str, Any], config: str) -> None:
    _submit(context, "run", {"config": config, "output": "out/records.json"})
    assert context["response"].status_code == 303


@when("the job finishes")
def job_finishes(context: dict[str, Any]) -> None:
    job = _job(context)
    deadline = time.monotonic() + _FINISH_TIMEOUT_S
    while job.running and time.monotonic() < deadline:
        time.sleep(0.01)
    assert not job.running, "the job never finished"


@when("I read the job's live log until it ends")
def read_live_log(context: dict[str, Any]) -> None:
    data: list[str] = []
    status = None
    with _client(context).stream(
        "GET", f"/jobs/{context['job_id']}/events"
    ) as response:
        assert response.headers["content-type"].startswith("text/event-stream")
        event = "message"
        for line in response.iter_lines():
            if line.startswith("event: "):
                event = line[len("event: ") :]
            elif line.startswith("data: "):
                value = line[len("data: ") :]
                if event == "done":
                    status = value
                    break
                data.append(value)
            elif not line:
                event = "message"
    context["live_log"] = data
    context["live_status"] = status


@when("I press Stop on the job")
def press_stop(context: dict[str, Any]) -> None:
    response = _post(context, f"/jobs/{context['job_id']}/stop", {})
    assert response.status_code == 303


@when("I press Force stop on the job")
def press_force_stop(context: dict[str, Any]) -> None:
    response = _post(context, f"/jobs/{context['job_id']}/kill", {})
    assert response.status_code == 303


@when("the GUI shuts down")
def gui_shuts_down(context: dict[str, Any]) -> None:
    context["app"].state.jobs.shutdown()


@when(parsers.parse("I ask to open the job's \"{label}\" folder"))
def ask_open(context: dict[str, Any], label: str) -> None:
    context["response"] = _post(context, f"/jobs/{context['job_id']}/open/{label}", {})


@when(parsers.parse('another site submits the explore form for "{url}"'))
def cross_site_submit(context: dict[str, Any], url: str) -> None:
    context["response"] = _client(context).post(
        "/new/explore", data={"url": url}, headers={"origin": "https://evil.example"}
    )


@when(parsers.parse('I open the map page for "{url}" with the access token'))
def open_map(context: dict[str, Any], url: str) -> None:
    context["response"] = _client(context).get("/map", params={"url": url})


@when("a real browser fills in the explore form for the local site with a wiki")
def browser_fills_form(context: dict[str, Any]) -> None:
    from playwright.sync_api import sync_playwright

    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    context["browser"] = (pw, browser)
    page = browser.new_page()
    context["page"] = page
    page.goto(context["gui"].launch_url)
    page.get_by_role("link", name="Explore", exact=True).click()
    page.fill("#url", context["site_url"])
    page.fill("#max_states", "3")
    page.fill("#max_requests", "10")
    page.get_by_label("A browsable wiki", exact=True).check()
    context["wiki_dir"] = context["workdir"] / "e2e-wiki"
    page.get_by_label("A browsable wiki: folder").fill(str(context["wiki_dir"]))


@when("starts the job and waits for it to finish")
def browser_starts_job(context: dict[str, Any]) -> None:
    page = context["page"]
    page.get_by_role("button", name="Start").click()
    page.get_by_text("Where the output landed").wait_for(timeout=120_000)


# --- Then ----------------------------------------------------------------------


def _text(context: dict[str, Any]) -> str:
    return str(context["response"].text)


def _job_page(context: dict[str, Any]) -> str:
    response = _client(context).get(f"/jobs/{context['job_id']}")
    assert response.status_code == 200
    return str(response.text)


@then(parsers.parse('the fake runner was started with "{command}"'))
def started_with(context: dict[str, Any], command: str) -> None:
    runner: FakeRunner = context["runner"]
    assert runner.started, "nothing was started"
    args, _ = runner.started[-1]
    assert args == _expected_args(context["workdir"], command)


@then("I am taken to that job's page, which shows the command")
def taken_to_job(context: dict[str, Any]) -> None:
    assert context["response"].headers["location"] == f"/jobs/{context['job_id']}"
    page = _job_page(context)
    assert "spoor explore http://127.0.0.1:9/app --max-states 5 --wiki" in page


@then("the fake runner was never started")
def never_started(context: dict[str, Any]) -> None:
    assert context["runner"].started == []


@then(parsers.parse("the response status is {status:d}"))
def response_status(context: dict[str, Any], status: int) -> None:
    assert context["response"].status_code == status


@then(parsers.parse('the page says "{message}"'))
def page_says(context: dict[str, Any], message: str) -> None:
    assert message in _text(context)


@then(parsers.parse('the preview reads "{command}"'))
def preview_reads(context: dict[str, Any], command: str) -> None:
    assert context["response"].status_code == 200
    assert context["response"].text == command


@then(parsers.parse('the fake runner was started with SPOOR_PROGRESS set to "{value}"'))
def started_with_progress(context: dict[str, Any], value: str) -> None:
    _, env = context["runner"].started[-1]
    assert env["SPOOR_PROGRESS"] == value


@then("the fake runner was started with a SPOOR_STOP_FILE that does not exist yet")
def started_with_stop_file(context: dict[str, Any]) -> None:
    _, env = context["runner"].started[-1]
    assert env["SPOOR_STOP_FILE"]
    assert not Path(env["SPOOR_STOP_FILE"]).exists()


@then(parsers.parse('the live log contains "{text}"'))
def live_log_contains(context: dict[str, Any], text: str) -> None:
    assert any(text in line for line in context["live_log"])


@then(parsers.parse('the live log never contains "{text}"'))
def live_log_never(context: dict[str, Any], text: str) -> None:
    assert not any(text in line for line in context["live_log"])
    assert text not in _job_page(context)


@then(parsers.parse('the live log ends with status "{status}"'))
def live_log_status(context: dict[str, Any], status: str) -> None:
    assert context["live_status"] == status


@then(parsers.parse('the job page shows status "{status}" with exit code {code:d}'))
def page_status_code(context: dict[str, Any], status: str, code: int) -> None:
    page = _job_page(context)
    assert f'status-{status}">{status.capitalize()}' in page
    assert f"exit code {code}" in page


@then(parsers.parse('the job page shows status "{status}"'))
def page_status(context: dict[str, Any], status: str) -> None:
    assert f'status-{status}">{status.capitalize()}' in _job_page(context)


@then(parsers.parse('the job page shows "{text}"'))
def page_shows(context: dict[str, Any], text: str) -> None:
    assert text in _job_page(context)


@then("the jobs page lists that job with its command")
def jobs_page_lists(context: dict[str, Any]) -> None:
    response = _client(context).get("/jobs")
    assert f'href="/jobs/{context["job_id"]}"' in response.text
    assert "spoor explore http://127.0.0.1:9/app" in response.text


@then("the job page shows the wiki folder's absolute path")
def shows_wiki_path(context: dict[str, Any]) -> None:
    assert _abs(context["workdir"], "out/wiki") in _job_page(context)


@then("the job page links to the wiki's index page")
def links_wiki(context: dict[str, Any]) -> None:
    assert f'href="/jobs/{context["job_id"]}/files/wiki/index.html"' in _job_page(
        context
    )


@then(parsers.parse('the job page links to the map for "{url}"'))
def links_map(context: dict[str, Any], url: str) -> None:
    assert 'href="/map?url=http%3A%2F%2F127.0.0.1%3A9%2Fapp"' in _job_page(context)


@then("the job's wiki index page is served")
def wiki_served(context: dict[str, Any]) -> None:
    response = _client(context).get(f"/jobs/{context['job_id']}/files/wiki/index.html")
    assert response.status_code == 200
    assert "Wiki index" in response.text


@then(parsers.parse('a request for "{rel}" under the job\'s wiki is refused'))
def wiki_traversal_refused(context: dict[str, Any], rel: str) -> None:
    encoded = rel.replace("/", "%2F")
    response = _client(context).get(f"/jobs/{context['job_id']}/files/wiki/{encoded}")
    assert response.status_code == 404
    assert "outside" not in response.text


@then("the folder opener was asked to open the job's wiki folder")
def opener_called(context: dict[str, Any]) -> None:
    assert context["response"].status_code == 303
    assert context["opened"] == [Path(_abs(context["workdir"], "out/wiki"))]


@then(parsers.parse('asking to open the job\'s "{label}" folder is refused'))
def open_refused(context: dict[str, Any], label: str) -> None:
    response = _post(context, f"/jobs/{context['job_id']}/open/{label}", {})
    assert response.status_code == 404
    assert len(context["opened"]) == 1


@then("the job's stop file was created")
def stop_file_created(context: dict[str, Any]) -> None:
    assert _job(context).stop_file.exists()


@then("the job page says what was mapped so far was saved")
def says_saved(context: dict[str, Any]) -> None:
    assert "What was mapped so far was saved." in _job_page(context)


@then("the fake process was killed")
def process_killed(context: dict[str, Any]) -> None:
    assert context["runner"].processes[-1].killed.is_set()


@then(parsers.parse('the page links to the explore form pre-filled with "{url}"'))
def links_prefilled(context: dict[str, Any], url: str) -> None:
    assert 'href="/new/explore?url=https%3A%2F%2Fshop.example%2Fproducts"' in _text(
        context
    )
    form = _client(context).get("/new/explore", params={"url": url})
    assert f'value="{url}"' in form.text


@then("the browser shows the job succeeded")
def browser_succeeded(context: dict[str, Any]) -> None:
    page = context["page"]
    assert page.locator(".status").first.inner_text() == "Succeeded", page.locator(
        "#log"
    ).inner_text()


@then("the browser shows where the wiki was written")
def browser_shows_wiki(context: dict[str, Any]) -> None:
    assert str(context["wiki_dir"]) in context["page"].content()


@then("the wiki folder contains an index page")
def wiki_has_index(context: dict[str, Any]) -> None:
    assert (context["wiki_dir"] / "index.html").is_file()
