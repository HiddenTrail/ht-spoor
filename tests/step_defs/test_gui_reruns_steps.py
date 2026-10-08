"""Step definitions for features/gui_reruns_and_browsing.feature (ROADMAP.md §2i).

Jobs run through gui-2's job manager with the shared fake runner (`_gui_fakes`);
forms are posted the way the GUI's own forms post them, with default output
folders under spoor-output/<date and time>/ like the GUI fills in. The folder
browser is exercised over real folders in a temp working folder. The `@browser`
scenario drives the real pop-up in a real browser.
"""

from __future__ import annotations

import html
import os
import re
import time
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Any

import pytest
from _gui_fakes import FINISH_TIMEOUT_S, FakeProcess, FakeRunner, flag_value
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenarios, then, when

from spoor.gui.app import create_app, token_cookie
from spoor.gui.job_routes import duration
from spoor.gui.job_routes import when as when_text
from spoor.gui.jobs import Job, JobManager
from spoor.gui.launch import start_gui
from spoor.security import storage
from spoor.serving.store import MapStore

scenarios("gui_reruns_and_browsing.feature")

_TOKEN = "known-test-token"
_PORT = 8769
_BASE = f"http://127.0.0.1:{_PORT}"
_URL = "http://127.0.0.1:9/app"
_STAMP = "2026-01-01_000000"
_CONFIG = "target: https://shop.example/products\nfields:\n  title: { selector: h2 }\n"


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


def _post(
    context: dict[str, Any], path: str, data: dict[str, str] | None = None
) -> Any:
    return _client(context).post(path, data=data or {}, headers={"origin": _BASE})


def _default(workdir: Path, *parts: str) -> str:
    """A default output path the way the GUI fills one in."""
    return str(workdir.joinpath("spoor-output", _STAMP, *parts))


def _readable(text: str) -> str:
    return " ".join(html.unescape(text).split())


def _job(context: dict[str, Any], index: int = 0) -> Job:
    return context["jobs"].all()[::-1][index]


# --- Given ---------------------------------------------------------------------


@given("the GUI app is running jobs with a fake runner")
def gui_with_fake_runner(context: dict[str, Any], workdir: Path) -> None:
    runner = FakeRunner()
    jobs = JobManager(runner, workdir)
    context.update(runner=runner, jobs=jobs, workdir=workdir)
    context["app"] = create_app(MapStore(), token=_TOKEN, port=_PORT, jobs=jobs)


@given("the fake command will write a scaffold and a wiki, record a map, and exit 0")
def fake_writes_outputs(context: dict[str, Any]) -> None:
    def script(proc: FakeProcess, args: Sequence[str], env: Any) -> None:
        wiki = Path(flag_value(args, "--wiki"))
        wiki.mkdir(parents=True, exist_ok=True)
        (wiki / "index.html").write_text("<h1>Wiki</h1>", encoding="utf-8")
        scaffold = Path(flag_value(args, "--scaffold"))
        scaffold.mkdir(parents=True, exist_ok=True)
        (scaffold / "interactive.yaml").write_text("fields: []\n", encoding="utf-8")
        MapStore().record(args[1], [])
        proc.exit(0)

    context["runner"].script = script


@given(parsers.parse('the working folder has a config "{relative}"'))
def has_config(workdir: Path, relative: str) -> None:
    path = workdir / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_CONFIG, encoding="utf-8")


@given(
    parsers.parse(
        'the working folder has the folders "{a}" and "{b}" and the file "{name}"'
    )
)
def has_folders_and_file(workdir: Path, a: str, b: str, name: str) -> None:
    (workdir / a).mkdir(exist_ok=True)
    (workdir / b).mkdir(exist_ok=True)
    (workdir / name).write_text("SECRET-FILE-CONTENT\n", encoding="utf-8")


@given(parsers.parse('the working folder has the folders "{a}" and "{b}"'))
def has_folders(workdir: Path, a: str, b: str) -> None:
    (workdir / a).mkdir(exist_ok=True)
    (workdir / b).mkdir(exist_ok=True)


@given(parsers.parse('the working folder has the file "{name}"'))
def has_file(workdir: Path, name: str) -> None:
    (workdir / name).write_text("x\n", encoding="utf-8")


@given("the GUI is running on loopback with the real command runner")
def real_gui(context: dict[str, Any], workdir: Path) -> None:
    context["workdir"] = workdir
    context["gui"] = start_gui(MapStore(), workdir=workdir)


# --- When: starting jobs ---------------------------------------------------------


def _start(context: dict[str, Any], kind: str, form: dict[str, str]) -> None:
    response = _post(context, f"/new/{kind}", form)
    assert response.status_code == 303, response.text
    context["forms"] = [*context.get("forms", []), form]


@when(parsers.parse('I start an explore job for "{url}"'))
def start_explore(context: dict[str, Any], url: str) -> None:
    _start(context, "explore", {"url": url})


@when("I start an explore job with a wiki and a scaffold")
def start_explore_outputs(context: dict[str, Any], workdir: Path) -> None:
    _start(
        context,
        "explore",
        {
            "url": _URL,
            "sandbox": "on",
            "session": "customer",
            "wiki": "on",
            "wiki_dir": _default(workdir, "wiki"),
            "scaffold": "on",
            "scaffold_dir": _default(workdir, "scaffold"),
        },
    )


@when(parsers.parse('I start an explore job for "{url}" with the wiki in "{rel}"'))
def start_explore_own_folder(context: dict[str, Any], url: str, rel: str) -> None:
    _start(context, "explore", {"url": url, "wiki": "on", "wiki_dir": rel})


@when("I start an explore job with every option set")
def start_explore_everything(context: dict[str, Any], workdir: Path) -> None:
    context["full_form"] = {
        "url": _URL,
        "sandbox": "on",
        "max_states": "5",
        "max_requests": "40",
        "max_seconds": "90",
        "max_depth": "2",
        "resume_from": "id:ab12",
        "session": "customer",
        "wiki": "on",
        "wiki_dir": _default(workdir, "wiki"),
        "screenshots": "on",
        "gen_tests": "on",
        "gen_tests_dir": _default(workdir, "tests"),
        "assert_no_new_signals": "on",
        "scaffold": "on",
        "scaffold_dir": _default(workdir, "scaffold"),
        "include_elements": "Buy*\nDetails",
        "exclude_elements": "Logout",
    }
    _start(context, "explore", context["full_form"])


@when(parsers.parse('I start a run job for "{config}"'))
def start_run(context: dict[str, Any], workdir: Path, config: str) -> None:
    _start(context, "run", {"config": config, "output": _default(workdir, "out.json")})


@when(parsers.parse('I start a run job for "{config}" as "{fmt}" into "{out}"'))
def start_run_format(context: dict[str, Any], config: str, fmt: str, out: str) -> None:
    _start(context, "run", {"config": config, "output": out, "format": fmt})


@when("the job finishes")
def job_finishes(context: dict[str, Any]) -> None:
    job = _job(context)
    deadline = time.monotonic() + FINISH_TIMEOUT_S
    while job.running and time.monotonic() < deadline:
        time.sleep(0.01)
    assert not job.running


# --- When: the menu --------------------------------------------------------------


_ITEM = re.compile(
    r'<form method="post" action="(?P<post>[^"]+)">\s*'
    r'<button type="submit" class="menu-item">(?P<plabel>[^<]+)</button>'
    r'|<a class="menu-item" href="(?P<get>[^"]+)">(?P<glabel>[^<]+)</a>'
)


def _menu(page: str) -> dict[str, tuple[str, str]]:
    """Label → (method, href) of every item in the page's "…" menus."""
    items: dict[str, tuple[str, str]] = {}
    for m in _ITEM.finditer(page):
        if m["post"]:
            items[m["plabel"]] = ("post", html.unescape(m["post"]))
        else:
            items[m["glabel"]] = ("get", html.unescape(m["get"]))
    return items


def _job_page(context: dict[str, Any], job: Job | None = None) -> str:
    job = job or _job(context)
    response = _client(context).get(f"/jobs/{job.id}")
    assert response.status_code == 200
    return str(response.text)


@when(parsers.parse('I choose "{label}" for the job'))
def choose(context: dict[str, Any], label: str) -> None:
    method, href = _menu(_job_page(context))[label]
    if method == "post":
        context["response"] = _post(context, href)
    else:
        context["response"] = _client(context).get(href)


@when("another site asks to rerun the job")
def cross_site_rerun(context: dict[str, Any]) -> None:
    context["response"] = _client(context).post(
        f"/jobs/{_job(context).id}/rerun", headers={"origin": "https://evil.example"}
    )


@when(parsers.parse('I ask to rerun the job "{job_id}"'))
def rerun_unknown(context: dict[str, Any], job_id: str) -> None:
    context["response"] = _post(context, f"/jobs/{job_id}/rerun")


@when("I open the explore form")
def open_explore(context: dict[str, Any]) -> None:
    context["response"] = _client(context).get("/new/explore")


@when("I open the extract form")
def open_extract(context: dict[str, Any]) -> None:
    context["response"] = _client(context).get("/new/run")


# --- When: browsing --------------------------------------------------------------


def _tree(folder: Path) -> list[str]:
    return sorted(str(p.relative_to(folder)) for p in folder.rglob("*"))


def _browse(context: dict[str, Any], path: str, mode: str) -> None:
    context["before"] = _tree(context["workdir"])
    response = _client(context).get("/browse", params={"path": path, "mode": mode})
    assert response.status_code == 200
    context["response"] = response
    context["listing"] = response.json()


@when("I browse the working folder for a folder")
def browse_folder(context: dict[str, Any], workdir: Path) -> None:
    _browse(context, str(workdir), "dir")


@when("I browse the working folder for a YAML file")
def browse_file(context: dict[str, Any], workdir: Path) -> None:
    _browse(context, str(workdir), "file")


@when("I browse without a starting folder")
def browse_default(context: dict[str, Any]) -> None:
    _browse(context, "", "dir")


@when("I browse starting from a folder that doesn't exist inside the working folder")
def browse_missing(context: dict[str, Any], workdir: Path) -> None:
    _browse(context, str(workdir / "nope" / "deeper"), "dir")


@when("a real browser opens the explore form and browses for the wiki folder")
def browser_browses(context: dict[str, Any]) -> None:
    from playwright.sync_api import sync_playwright

    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    context["browser"] = (pw, browser)
    page = browser.new_page()
    context["page"] = page
    page.goto(context["gui"].launch_url)
    page.get_by_role("link", name="Explore", exact=True).click()
    page.fill("#wiki_dir", str(context["workdir"]))
    page.locator('button[data-target="wiki_dir"]').click()
    page.locator("#folder-browser .fb-entry", has_text="alpha").wait_for()


@when(parsers.parse('opens "{name}" and chooses it with the new folder name "{new}"'))
def browser_chooses(context: dict[str, Any], name: str, new: str) -> None:
    page = context["page"]
    page.locator("#folder-browser .fb-entry", has_text=name).click()
    page.locator("#folder-browser .fb-path", has_text=name).wait_for()
    page.fill("#folder-browser .fb-new", new)
    page.get_by_role("button", name="Choose this folder").click()


# --- Then ------------------------------------------------------------------------


def _text(context: dict[str, Any]) -> str:
    return str(context["response"].text)


@then("the jobs list shows that job's start date and time")
def list_shows_when(context: dict[str, Any]) -> None:
    page = _client(context).get("/jobs").text
    stamp = when_text(_job(context).started_at)
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", stamp)
    assert stamp in page


@then("the jobs list shows that job's duration")
def list_shows_duration(context: dict[str, Any]) -> None:
    page = _client(context).get("/jobs").text
    assert "<th>Duration</th>" in page
    assert duration(_job(context)) in page


@then("the job page shows when it started and when it finished")
def page_shows_times(context: dict[str, Any]) -> None:
    job = _job(context)
    text = _readable(_job_page(context))
    assert f"Started {when_text(job.started_at)}" in text
    assert f"finished {when_text(job.finished_at)}" in text


def _labels(raw: str) -> list[str]:
    return re.findall(r'"([^"]+)"', raw)


@then(parsers.re(r"the job's menu offers (?P<raw>.+)$"))
def menu_offers(context: dict[str, Any], raw: str) -> None:
    menu = _menu(_job_page(context))
    for label in _labels(raw):
        assert label in menu, f"{label} not in {list(menu)}"


@then("the jobs list offers the same menu for that job")
def list_menu(context: dict[str, Any]) -> None:
    page = _client(context).get("/jobs").text
    assert set(_menu(page)) == set(_menu(_job_page(context)))


@then(parsers.parse('the job\'s menu does not offer "{label}"'))
def menu_lacks(context: dict[str, Any], label: str) -> None:
    assert label not in _menu(_job_page(context))


@then(parsers.parse('"Edit config" opens the editor for "{relative}"'))
def edit_config_link(context: dict[str, Any], relative: str) -> None:
    _, href = _menu(_job_page(context))["Edit config"]
    assert href == "/configs/edit?path=configs%2Fshop.yaml"
    response = _client(context).get(href)
    assert response.status_code == 200
    assert "target: https://shop.example" in response.text


def _same_but_stamp(first: str, second: str, workdir: Path) -> bool:
    root = str(workdir / "spoor-output")
    if first == second:
        return True
    if not (first.startswith(root) and second.startswith(root)):
        return False
    a, b = Path(first).relative_to(root).parts, Path(second).relative_to(root).parts
    return a[1:] == b[1:] and a[0] != b[0]


@then("a second job was started with the same settings")
def second_job_same(context: dict[str, Any], workdir: Path) -> None:
    started = context["runner"].started
    assert len(started) == 2
    first, second = started[0][0], started[1][0]
    assert len(first) == len(second)
    assert all(
        _same_but_stamp(a, b, workdir) for a, b in zip(first, second, strict=True)
    )


@then("its default output folders are in a new date-and-time folder")
def fresh_folders(context: dict[str, Any], workdir: Path) -> None:
    root = workdir / "spoor-output"
    if context["response"].status_code == 303:
        values = _job(context, 1).spec.form
    else:
        values = _form_values(_text(context))
    for name in ("wiki_dir", "scaffold_dir"):
        new = Path(values[name])
        assert new.is_relative_to(root), values[name]
        assert new.relative_to(root).parts[0] != _STAMP
        assert new.name == Path(_default(workdir, name.split("_")[0])).name


@then("I am taken to the new job's page")
def to_new_job(context: dict[str, Any]) -> None:
    response = context["response"]
    assert response.status_code == 303
    assert response.headers["location"] == f"/jobs/{_job(context, 1).id}"


@then(parsers.parse('the second job writes its wiki to "{rel}" again'))
def same_own_folder(context: dict[str, Any], workdir: Path, rel: str) -> None:
    assert _job(context, 1).spec.outputs["wiki"] == Path(os.path.abspath(workdir / rel))
    assert (
        _job(context, 0).spec.outputs["wiki"] == _job(context, 1).spec.outputs["wiki"]
    )


@then(parsers.parse("the response status is {status:d}"))
def response_status(context: dict[str, Any], status: int) -> None:
    assert context["response"].status_code == status


@then("only one job was ever started")
def one_job(context: dict[str, Any]) -> None:
    assert len(context["runner"].started) == 1


def _form_values(page: str) -> dict[str, str]:
    """A form page's filled-in values: inputs, checkboxes, text areas, select."""
    values: dict[str, str] = {}
    for m in re.finditer(r"<input\b[^>]*>", page, re.S):
        tag = m.group(0)
        name = re.search(r'name="([^"]+)"', tag)
        if not name:
            continue
        if 'type="checkbox"' in tag:
            values[name[1]] = "on" if " checked" in tag else ""
        else:
            value = re.search(r'value="([^"]*)"', tag)
            values[name[1]] = html.unescape(value[1]) if value else ""
    for m in re.finditer(
        r'<textarea[^>]*name="([^"]+)"[^>]*>(.*?)</textarea>', page, re.S
    ):
        values[m[1]] = html.unescape(m[2])
    selected = re.search(r'<option value="([^"]*)" selected', page)
    if selected:
        values["format"] = selected[1]
    return values


@then("the explore form is filled in with every original value")
def explore_prefilled(context: dict[str, Any]) -> None:
    assert context["response"].status_code == 200
    values = _form_values(_text(context))
    for name, original in context["full_form"].items():
        if name in ("wiki_dir", "gen_tests_dir", "scaffold_dir"):
            continue  # moved to a fresh folder; checked separately
        assert values.get(name) == original, (name, values.get(name), original)


@then(
    parsers.parse(
        'the extract form has the config "{config}", the output "{out}" '
        'and the format "{fmt}"'
    )
)
def extract_prefilled(context: dict[str, Any], config: str, out: str, fmt: str) -> None:
    values = _form_values(_text(context))
    assert values["config"] == config
    assert values["output"] == out
    assert values["format"] == fmt


@then(
    "the apply-scaffold form has the exploration's address, "
    "its scaffold file and its wiki"
)
def apply_prefilled(context: dict[str, Any], workdir: Path) -> None:
    values = _form_values(_text(context))
    assert values["url"] == _URL
    assert values["scaffold"] == str(
        Path(os.path.abspath(_default(workdir, "scaffold"))) / "interactive.yaml"
    )
    assert values["wiki"] == "on"
    assert values["wiki_dir"] == os.path.abspath(_default(workdir, "wiki"))


@then("the apply-scaffold form keeps the exploration's sandbox and login choices")
def apply_keeps(context: dict[str, Any]) -> None:
    values = _form_values(_text(context))
    assert values["sandbox"] == "on"
    assert values["session"] == "customer"


def _has_browse(page: str, target: str, mode: str) -> bool:
    pattern = rf'data-browse="{mode}"\s+data-target="{target}"'
    return re.search(pattern, page) is not None


@then(
    "the wiki, tests and scaffold folder fields each have a Browse button for a folder"
)
def explore_browse(context: dict[str, Any]) -> None:
    page = _text(context)
    for target in ("wiki_dir", "gen_tests_dir", "scaffold_dir"):
        assert _has_browse(page, target, "dir"), target


@then("the config field has a Browse button for a YAML file")
def config_browse(context: dict[str, Any]) -> None:
    assert _has_browse(_text(context), "config", "file")


@then(
    "the records and healing report fields have a Browse button "
    "that keeps the file name"
)
def save_browse(context: dict[str, Any]) -> None:
    page = _text(context)
    assert _has_browse(page, "output", "save")
    assert _has_browse(page, "healing_report_path", "save")


def _names(context: dict[str, Any], key: str) -> list[str]:
    return [entry["name"] for entry in context["listing"][key]]


@then(parsers.parse('the listing shows the folders "{a}" and "{b}"'))
def listing_folders(context: dict[str, Any], a: str, b: str) -> None:
    assert _names(context, "folders") == [a, b]


@then(parsers.parse('the listing does not show "{name}"'))
def listing_lacks(context: dict[str, Any], name: str) -> None:
    assert name not in _names(context, "folders") + _names(context, "files")


@then("the listing names the working folder's parent")
def listing_parent(context: dict[str, Any], workdir: Path) -> None:
    assert context["listing"]["parent"] == str(workdir.parent)


@then(parsers.parse('the listing shows the file "{name}"'))
def listing_file(context: dict[str, Any], name: str) -> None:
    assert name in _names(context, "files")


@then("the listing is for the working folder")
def listing_is_workdir(context: dict[str, Any], workdir: Path) -> None:
    assert context["listing"]["path"] == str(workdir)


@then("the listing contains no file contents")
def listing_no_contents(context: dict[str, Any]) -> None:
    assert "SECRET-FILE-CONTENT" not in _text(context)
    for entry in context["listing"]["files"] + context["listing"]["folders"]:
        assert set(entry) == {"name", "path"}


@then("browsing changed nothing in the working folder")
def browsing_wrote_nothing(context: dict[str, Any]) -> None:
    assert _tree(context["workdir"]) == context["before"]


@then(
    parsers.parse(
        'the wiki folder field holds the "{rel}" folder inside the working folder'
    )
)
def browser_field(context: dict[str, Any], rel: str) -> None:
    value = context["page"].input_value("#wiki_dir")
    assert value == str(context["workdir"].joinpath(*rel.split("/")))
    # Choosing doesn't create anything: Spoor makes the folder when a run writes.
    assert not Path(value).exists()
