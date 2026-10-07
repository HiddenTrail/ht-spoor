"""Step definitions for features/gui_sessions_configs.feature (ROADMAP.md §2i, gui-3).

Saved logins: the session commands run through gui-2's job manager with the
shared fake runner (`_gui_fakes`), which records the arguments and plays a
scripted process; the listing reads a real session store under a temp cache.
Config files: real files in a temp working folder, edited through the GUI's
endpoints. The `@browser` scenarios run the real CLI and a real browser.
"""

from __future__ import annotations

import json
import os
import shlex
from collections.abc import Iterator, Mapping, Sequence
from pathlib import Path
from typing import Any

import pytest
from _gui_fakes import FakeProcess, FakeRunner
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenarios, then, when

from spoor.gui.app import create_app, token_cookie
from spoor.gui.jobs import JobManager
from spoor.gui.launch import start_gui
from spoor.security import storage
from spoor.security.session_store import SessionStore
from spoor.serving.store import MapStore

scenarios("gui_sessions_configs.feature")

_TOKEN = "known-test-token"
_PORT = 8767
_BASE = f"http://127.0.0.1:{_PORT}"
_VALID = "target: https://shop.example/products\nfields:\n  title: { selector: h2 }\n"
_INVALID = "fields: {}\n"


def _upload_arg(args: Sequence[str]) -> Path:
    """The uploaded file's path in a `session add` command (first value after --)."""
    return Path(args[args.index("--") + 1])


def _storage_state(marker: str) -> dict[str, object]:
    return {
        "cookies": [{"name": "session", "value": marker, "domain": "x", "path": "/"}],
        "origins": [],
    }


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
    monkeypatch.setattr(storage, "CACHE_ROOT", workdir / ".spoor-cache")


def _client(context: dict[str, Any]) -> TestClient:
    client = TestClient(context["app"], base_url=_BASE, follow_redirects=False)
    client.cookies.set(token_cookie(_PORT), _TOKEN)
    return client


def _post(context: dict[str, Any], path: str, **kwargs: Any) -> Any:
    return _client(context).post(path, headers={"origin": _BASE}, **kwargs)


# --- Given ---------------------------------------------------------------------


@given("the GUI app is running jobs with a fake runner")
def gui_with_fake_runner(context: dict[str, Any], workdir: Path) -> None:
    runner = FakeRunner()
    jobs = JobManager(runner, workdir)
    context.update(runner=runner, jobs=jobs, workdir=workdir)
    context["app"] = create_app(MapStore(), token=_TOKEN, port=_PORT, jobs=jobs)


@given(
    parsers.parse(
        'a login "{label}" is stored for "{site}" with the secret marker "{marker}"'
    )
)
def stored_login(label: str, site: str, marker: str) -> None:
    SessionStore().add(site, label, _storage_state(marker))


@given("the fake command will report the upload it was given and exit 0")
def fake_reports_upload(context: dict[str, Any]) -> None:
    def script(proc: FakeProcess, args: Sequence[str], env: Mapping[str, str]) -> None:
        upload = _upload_arg(args)
        context["upload_path"] = upload
        context["upload_seen"] = upload.read_text(encoding="utf-8")
        proc.emit(f"Stored session {args[3]!r} for {args[-1]}.")
        proc.exit(0)

    context["runner"].script = script


@given(parsers.parse('the fake command will print "{line}" and exit {code:d}'))
def fake_prints(context: dict[str, Any], line: str, code: int) -> None:
    def script(proc: FakeProcess, args: Sequence[str], env: Any) -> None:
        context["upload_path"] = _upload_arg(args) if "--" in args else None
        proc.emit(line)
        proc.exit(code)

    context["runner"].script = script


@given("the fake command keeps running until it is killed")
def fake_waits_for_kill(context: dict[str, Any]) -> None:
    def script(proc: FakeProcess, args: Sequence[str], env: Any) -> None:
        context["upload_path"] = _upload_arg(args)
        proc.killed.wait(10)
        proc.exit(1)

    context["runner"].script = script


@given(parsers.parse("the GUI waits at most {seconds:f} seconds for a login command"))
def short_wait(context: dict[str, Any], seconds: float) -> None:
    context["jobs"].quick_command_seconds = seconds


def _write(workdir: Path, relative: str, text: str) -> None:
    path = workdir / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@given(parsers.parse('the working folder has a valid config "{relative}"'))
def valid_config(workdir: Path, relative: str) -> None:
    _write(workdir, relative, _VALID)


@given(
    parsers.parse(
        'the working folder has a valid config "{relative}" with a header "{header}"'
    )
)
def valid_config_with_header(workdir: Path, relative: str, header: str) -> None:
    name, value = header.split(": ", 1)
    _write(workdir, relative, _VALID + f'headers:\n  {name}: "{value}"\n')


@given(parsers.parse('the working folder has an invalid config "{relative}"'))
def invalid_config(workdir: Path, relative: str) -> None:
    _write(workdir, relative, _INVALID)


@given(parsers.parse('a file exists at "{relative}" relative to the working folder'))
def file_exists(workdir: Path, relative: str) -> None:
    # Real files, so a 404 can only come from the GUI refusing the path, never
    # from the file simply not being there.
    _write(workdir, relative, _VALID)
    assert (workdir / relative).is_file()


@given(parsers.parse('the working folder has a YAML file "{relative}"'))
def other_yaml(workdir: Path, relative: str) -> None:
    _write(workdir, relative, "fields: {}\n")


@given("the GUI is running on loopback with the real command runner")
def real_gui(context: dict[str, Any], workdir: Path) -> None:
    context["workdir"] = workdir
    context["gui"] = start_gui(MapStore(), workdir=workdir)


@given(parsers.parse('a captured login file for "{site}" marked "{marker}"'))
def captured_login_file(context: dict[str, Any], workdir: Path, marker: str) -> None:
    path = workdir / "captured" / "state.json"
    path.parent.mkdir()
    path.write_text(json.dumps(_storage_state(marker)), encoding="utf-8")
    context["login_file"] = path


# --- When ----------------------------------------------------------------------


def _add_login(context: dict[str, Any], label: str, site: str, with_file: bool) -> None:
    files = (
        {"file": ("state.json", json.dumps(_storage_state("UPLOADED")), "text/json")}
        if with_file
        else None
    )
    context["response"] = _post(
        context, "/logins/add", data={"label": label, "site": site}, files=files
    )


@when(
    # A regex, not `parse`, so an empty name ("") matches too.
    parsers.re(
        r'I add a login "(?P<label>[^"]*)" for "(?P<site>[^"]+)" '
        r"from an uploaded file"
    )
)
def add_login(context: dict[str, Any], label: str, site: str) -> None:
    _add_login(context, label, site, with_file=True)


@when(parsers.parse('I add a login "{label}" for "{site}" without a file'))
def add_login_no_file(context: dict[str, Any], label: str, site: str) -> None:
    _add_login(context, label, site, with_file=False)


@when(parsers.parse('I remove the login "{label}" for "{site}"'))
def remove_login(context: dict[str, Any], label: str, site: str) -> None:
    context["response"] = _post(
        context, "/logins/remove", data={"site": site, "label": label}
    )


@when("I open the logins page")
def open_logins(context: dict[str, Any]) -> None:
    context["response"] = _client(context).get("/logins")


@when("I open the explore form")
def open_explore(context: dict[str, Any]) -> None:
    context["response"] = _client(context).get("/new/explore")


@when(parsers.parse('another site posts a login "{label}" for "{site}"'))
def cross_site_login(context: dict[str, Any], label: str, site: str) -> None:
    context["response"] = _client(context).post(
        "/logins/add",
        data={"label": label, "site": site},
        files={"file": ("s.json", "{}", "text/json")},
        headers={"origin": "https://evil.example"},
    )


@when("I open the configs page")
def open_configs(context: dict[str, Any]) -> None:
    context["response"] = _client(context).get("/configs")


@when(parsers.parse('I open the config "{relative}"'))
def open_config(context: dict[str, Any], relative: str) -> None:
    context["response"] = _client(context).get(
        "/configs/edit", params={"path": relative}
    )


@when(parsers.parse('I check the config "{relative}" with the text:'))
def check_config(context: dict[str, Any], relative: str, docstring: str) -> None:
    context["before"] = (context["workdir"] / relative).read_bytes()
    context["response"] = _post(
        context, "/configs/check", data={"path": relative, "text": docstring}
    )


@when(parsers.parse('I save the config "{relative}" with the text:'))
def save_config(context: dict[str, Any], relative: str, docstring: str) -> None:
    context["response"] = _post(
        context, "/configs/save", data={"path": relative, "text": docstring}
    )


@when(parsers.parse('I create the config "{relative}"'))
def create_config(context: dict[str, Any], relative: str) -> None:
    context["response"] = _post(context, "/configs/new", data={"path": relative})


@when(parsers.parse('I open the extract form for the config "{relative}"'))
def open_extract_for(context: dict[str, Any], relative: str) -> None:
    context["response"] = _client(context).get(
        "/new/run", params={"config": relative}
    )


def _browser_page(context: dict[str, Any]) -> Any:
    from playwright.sync_api import sync_playwright

    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    context["browser"] = (pw, browser)
    page = browser.new_page()
    page.goto(context["gui"].launch_url)
    context["page"] = page
    return page


@when(parsers.parse('a real browser adds that login as "{label}" for "{site}"'))
def browser_adds_login(context: dict[str, Any], label: str, site: str) -> None:
    page = _browser_page(context)
    page.get_by_role("link", name="Logins", exact=True).click()
    page.fill("#label", label)
    page.fill("#site", site)
    page.set_input_files("#file", str(context["login_file"]))
    page.get_by_role("button", name="Add login").click()
    page.wait_for_load_state()


@when(parsers.parse('a real browser opens "{relative}" in the editor'))
def browser_opens_config(context: dict[str, Any], relative: str) -> None:
    page = _browser_page(context)
    page.get_by_role("link", name="Configs", exact=True).click()
    page.get_by_role("link", name=relative).click()


@when("replaces its text with a valid config and saves")
def browser_saves(context: dict[str, Any]) -> None:
    page = context["page"]
    page.get_by_label("Config text").fill(_VALID)
    page.get_by_role("button", name="Save").click()
    page.wait_for_load_state()


# --- Then ----------------------------------------------------------------------


def _text(context: dict[str, Any]) -> str:
    return str(context["response"].text)


@then(parsers.parse('the page lists the login "{label}" for "{site}"'))
def lists_login(context: dict[str, Any], label: str, site: str) -> None:
    text = _text(context)
    assert f"<td>{site}</td>" in text
    assert f"<strong>{label}</strong>" in text


@then(parsers.parse('the page never shows "{value}"'))
def never_shows(context: dict[str, Any], value: str) -> None:
    assert value not in _text(context)


@then(parsers.parse('the page says "{message}"'))
def page_says(context: dict[str, Any], message: str) -> None:
    assert message in _text(context), _text(context)


@then(parsers.parse('the fake runner was started with "{command}"'))
def started_with(context: dict[str, Any], command: str) -> None:
    args, _ = context["runner"].started[-1]
    expected = [
        str(context["upload_path"]) if token == "<upload>" else token
        for token in shlex.split(command)
    ]
    assert args == expected


@then("the command saw the uploaded file's contents")
def saw_upload(context: dict[str, Any]) -> None:
    assert "UPLOADED" in context["upload_seen"]


@then("the temporary copy of the upload is gone")
def upload_gone(context: dict[str, Any]) -> None:
    upload: Path = context["upload_path"]
    assert not upload.exists()
    assert not upload.parent.exists()
    assert not upload.is_relative_to(context["workdir"])


@then(parsers.parse("the response status is {status:d}"))
def response_status(context: dict[str, Any], status: int) -> None:
    assert context["response"].status_code == status


@then("the fake runner was never started")
def never_started(context: dict[str, Any]) -> None:
    assert context["runner"].started == []


@then("the fake process was killed")
def process_killed(context: dict[str, Any]) -> None:
    assert context["runner"].processes[-1].killed.is_set()


@then(parsers.parse('the page offers the login name "{label}"'))
def offers_login(context: dict[str, Any], label: str) -> None:
    text = _text(context)
    assert 'list="saved-logins"' in text
    assert f'<option value="{label}">' in text


@then(parsers.parse('the page lists the config "{relative}" as valid'))
def lists_valid(context: dict[str, Any], relative: str) -> None:
    row = _row(_text(context), relative)
    assert "valid" in row and "not valid" not in row


@then(parsers.parse('the page lists the config "{relative}" as not valid'))
def lists_invalid(context: dict[str, Any], relative: str) -> None:
    assert "not valid" in _row(_text(context), relative)


def _row(text: str, relative: str) -> str:
    marker = f">{relative}</a>"
    assert marker in text, f"{relative} not listed"
    start = text.index(marker)
    return text[start : text.index("</tr>", start)]


@then(parsers.parse('the page does not list "{relative}"'))
def not_listed(context: dict[str, Any], relative: str) -> None:
    assert f">{relative}</a>" not in _text(context)


@then(parsers.parse('the editor contains "{value}"'))
def editor_contains(context: dict[str, Any], value: str) -> None:
    assert context["response"].status_code == 200
    assert value in _text(context)


@then(parsers.parse('the config file "{relative}" is unchanged'))
def unchanged(context: dict[str, Any], relative: str) -> None:
    assert (context["workdir"] / relative).read_bytes() == context["before"]


@then(parsers.parse('the config file "{relative}" contains "{value}"'))
def file_contains(context: dict[str, Any], relative: str, value: str) -> None:
    assert value in (context["workdir"] / relative).read_text(encoding="utf-8")


@then(parsers.parse('the page links to the extract form pre-filled with "{relative}"'))
def links_run(context: dict[str, Any], relative: str) -> None:
    assert 'href="/new/run?config=configs%2Fshop.yaml"' in _text(context)


@then(parsers.parse('I am taken to the editor for "{relative}"'))
def taken_to_editor(context: dict[str, Any], relative: str) -> None:
    response = context["response"]
    assert response.status_code == 303
    assert response.headers["location"] == "/configs/edit?path=configs%2Fnew.yaml"


@then(parsers.parse('no file "{relative}" was written'))
def nothing_written(context: dict[str, Any], relative: str) -> None:
    assert not os.path.exists(context["workdir"] / relative)


@then(parsers.parse('the config field is pre-filled with "{relative}"'))
def config_prefilled(context: dict[str, Any], relative: str) -> None:
    assert f'name="config" value="{relative}"' in _text(context)


@then(parsers.parse('the browser lists the login "{label}" for "{site}"'))
def browser_lists(context: dict[str, Any], label: str, site: str) -> None:
    page = context["page"]
    row = page.locator("tr", has_text=site)
    assert row.count() == 1, page.content()
    assert label in row.inner_text()


@then(parsers.parse('the browser page never shows "{value}"'))
def browser_never(context: dict[str, Any], value: str) -> None:
    assert value not in context["page"].content()


@then(parsers.parse('the session store has the login "{label}" for "{site}"'))
def store_has(label: str, site: str) -> None:
    assert [m.label for m in SessionStore().list(site)] == [label]


@then(parsers.parse('the browser says "{message}"'))
def browser_says(context: dict[str, Any], message: str) -> None:
    assert message in context["page"].inner_text("main")
