"""Step definitions for features/gui_servers.feature (ROADMAP.md §2i, slice gui-4).

The map server is started through gui-2's job manager with the shared fake
runner (`_gui_fakes`) and an injected health check, so starting, readiness,
stopping and failure are pinned without a real server. The MCP scenario runs
the exact configuration the page shows, as a real MCP client would, from an
unrelated folder. The `@browser` scenario runs a real `spoor serve` started
from a real browser.
"""

from __future__ import annotations

import asyncio
import html
import json
import os
import re
import shlex
import socket
import subprocess
import sys
import time
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Any

import httpx
import pytest
from _gui_fakes import FINISH_TIMEOUT_S, FakeProcess, FakeRunner
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenarios, then, when

from spoor.gui.app import create_app, token_cookie
from spoor.gui.jobs import JobManager
from spoor.gui.launch import start_gui
from spoor.security import storage
from spoor.serving.store import MapStore

scenarios("gui_servers.feature")

_TOKEN = "known-test-token"
_PORT = 8768
_BASE = f"http://127.0.0.1:{_PORT}"


@pytest.fixture
def context() -> Iterator[dict[str, Any]]:
    ctx: dict[str, Any] = {"healthy": False}
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


def _text(context: dict[str, Any]) -> str:
    return str(context["response"].text)


# --- Given ---------------------------------------------------------------------


@given("the GUI app is running jobs with a fake runner")
def gui_with_fake_runner(context: dict[str, Any], workdir: Path) -> None:
    runner = FakeRunner()
    jobs = JobManager(runner, workdir)
    context.update(runner=runner, jobs=jobs, workdir=workdir)
    context["app"] = create_app(
        MapStore(),
        token=_TOKEN,
        port=_PORT,
        jobs=jobs,
        health=lambda port: bool(context["healthy"]),
    )


@given("the fake command keeps running until it is killed")
def fake_waits_for_kill(context: dict[str, Any]) -> None:
    def script(proc: FakeProcess, args: Sequence[str], env: Any) -> None:
        proc.killed.wait(FINISH_TIMEOUT_S)
        proc.exit(1)

    context["runner"].script = script


@given(parsers.parse('the fake command will print "{line}" and exit {code:d}'))
def fake_prints(context: dict[str, Any], line: str, code: int) -> None:
    def script(proc: FakeProcess, args: Sequence[str], env: Any) -> None:
        proc.emit(line)
        proc.exit(code)

    context["runner"].script = script


@given("the map server's health check does not answer yet")
def not_healthy(context: dict[str, Any]) -> None:
    context["healthy"] = False


@given("the map server's health check answers")
def healthy(context: dict[str, Any]) -> None:
    context["healthy"] = True


@given(parsers.parse('a map store that has mapped "{url}"'))
def mapped(url: str) -> None:
    MapStore().record(url, [{"title": "Blue mug"}], tier=1)


@given("the GUI is running on loopback with the real command runner")
def real_gui(context: dict[str, Any], workdir: Path) -> None:
    context["workdir"] = workdir
    context["gui"] = start_gui(MapStore(), workdir=workdir)


# --- When ----------------------------------------------------------------------


def _start(context: dict[str, Any], port: str, *, recheck: bool = False) -> None:
    data = {"port": port}
    if recheck:
        data["recheck"] = "on"
    context["response"] = _client(context).post(
        "/servers/start", data=data, headers={"origin": _BASE}
    )


@when(parsers.re(r'I start the map server on port "(?P<port>[^"]*)"$'))
def start_server(context: dict[str, Any], port: str) -> None:
    _start(context, port)


@when(
    parsers.parse(
        'I start the map server on port "{port}" with re-checking allowed'
    )
)
def start_server_recheck(context: dict[str, Any], port: str) -> None:
    _start(context, port, recheck=True)


@when("I open the servers page")
def open_servers(context: dict[str, Any]) -> None:
    context["response"] = _client(context).get("/servers")


@when("I stop the map server")
def stop_server(context: dict[str, Any]) -> None:
    response = _client(context).post("/servers/stop", headers={"origin": _BASE})
    assert response.status_code == 303
    context["response"] = _client(context).get("/servers")


@when("the server job finishes")
def server_job_finishes(context: dict[str, Any]) -> None:
    job = context["jobs"].all()[0]
    deadline = time.monotonic() + FINISH_TIMEOUT_S
    while job.running and time.monotonic() < deadline:
        time.sleep(0.01)
    assert not job.running


@when(parsers.parse('another site starts the map server on port "{port}"'))
def cross_site_start(context: dict[str, Any], port: str) -> None:
    context["response"] = _client(context).post(
        "/servers/start", data={"port": port}, headers={"origin": "https://evil.example"}
    )


def _mcp_config(context: dict[str, Any]) -> dict[str, Any]:
    page = _client(context).get("/servers").text
    match = re.search(r'<pre id="mcp-json">(.*?)</pre>', page, re.S)
    assert match, "no MCP configuration on the page"
    config: dict[str, Any] = json.loads(html.unescape(match.group(1)))
    return dict(config["mcpServers"]["spoor"])


@when(
    "an MCP client runs the configuration from the servers page "
    "in an unrelated folder"
)
def mcp_client_runs(context: dict[str, Any], tmp_path: Path) -> None:
    from mcp import ClientSession
    from mcp.client.stdio import (
        StdioServerParameters,
        get_default_environment,
        stdio_client,
    )

    server = _mcp_config(context)
    elsewhere = tmp_path / "somewhere-else"
    elsewhere.mkdir()

    async def ask() -> str:
        params = StdioServerParameters(
            command=server["command"],
            args=server["args"],
            env={**get_default_environment(), **server["env"]},
            cwd=elsewhere,
        )
        async with (
            stdio_client(params) as (read, write),
            ClientSession(read, write) as session,
        ):
            await session.initialize()
            result = await session.call_tool("list_mapped_domains", {})
            return json.dumps(result.model_dump(mode="json"))

    context["mcp_answer"] = asyncio.run(asyncio.wait_for(ask(), timeout=60))
    # The folder it ran in really was unrelated: no cache appeared there.
    assert not (elsewhere / ".spoor-cache").exists()


@when("Spoor starts with SPOOR_CACHE_DIR set to a folder")
def start_with_env(context: dict[str, Any], tmp_path: Path) -> None:
    context["expected_cache"] = str(tmp_path / "my-cache")
    context["cache_seen"] = _cache_root_in_new_process(
        tmp_path, {"SPOOR_CACHE_DIR": context["expected_cache"]}
    )


@when("Spoor starts without SPOOR_CACHE_DIR")
def start_without_env(context: dict[str, Any], tmp_path: Path) -> None:
    context["cwd"] = tmp_path
    context["cache_seen"] = _cache_root_in_new_process(tmp_path, {})


def _cache_root_in_new_process(cwd: Path, extra: dict[str, str]) -> str:
    env = {k: v for k, v in os.environ.items() if k != "SPOOR_CACHE_DIR"}
    env.update(extra)
    out = subprocess.run(
        [
            sys.executable,
            "-c",
            "import os; from spoor.security import storage; "
            "print(os.path.abspath(storage.CACHE_ROOT))",
        ],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    return out.stdout.strip()


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


@when("a real browser starts the map server on a free port")
def browser_starts_server(context: dict[str, Any]) -> None:
    from playwright.sync_api import sync_playwright

    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    context["browser"] = (pw, browser)
    page = browser.new_page()
    context["page"] = page
    context["serve_port"] = _free_port()
    page.goto(context["gui"].launch_url)
    page.get_by_role("link", name="Servers", exact=True).click()
    page.fill("#port", str(context["serve_port"]))
    page.get_by_role("button", name="Start the map server").click()
    # The page refreshes itself while the server starts.
    page.get_by_text("The map server is running").wait_for(timeout=60_000)


@when("the browser stops the map server")
def browser_stops_server(context: dict[str, Any]) -> None:
    page = context["page"]
    page.get_by_role("button", name="Stop the map server").click()
    page.get_by_text("The map server is not running").wait_for(timeout=30_000)


# --- Then ----------------------------------------------------------------------


@then(parsers.parse('the fake runner was started with "{command}"'))
def started_with(context: dict[str, Any], command: str) -> None:
    args, _ = context["runner"].started[-1]
    assert args == shlex.split(command)


@then("I am taken back to the servers page")
def back_to_servers(context: dict[str, Any]) -> None:
    assert context["response"].status_code == 303
    assert context["response"].headers["location"] == "/servers"


@then("the page has no field for the server's address")
def no_host_field(context: dict[str, Any]) -> None:
    text = _text(context)
    assert 'name="port"' in text
    assert 'name="host"' not in text


@then(parsers.parse("the response status is {status:d}"))
def response_status(context: dict[str, Any], status: int) -> None:
    assert context["response"].status_code == status


@then(parsers.parse('the page says "{message}"'))
def page_says(context: dict[str, Any], message: str) -> None:
    assert message in _text(context), _text(context)


@then("the fake runner was never started")
def never_started(context: dict[str, Any]) -> None:
    assert context["runner"].started == []


@then(parsers.parse("the fake runner was started {count:d} time"))
def started_count(context: dict[str, Any], count: int) -> None:
    assert len(context["runner"].started) == count


@then("the page says the map server is starting")
def says_starting(context: dict[str, Any]) -> None:
    text = _text(context)
    assert "The map server is starting" in text
    assert 'http-equiv="refresh"' in text


@then(parsers.parse('the page says the map server is running at "{url}"'))
def says_running(context: dict[str, Any], url: str) -> None:
    text = _text(context)
    assert "The map server is running at" in text
    assert f">{url}</a>" in text


@then(parsers.parse('the page links to "{url}"'))
def links_to(context: dict[str, Any], url: str) -> None:
    assert f'href="{url}"' in _text(context)


@then("the fake process was killed")
def killed(context: dict[str, Any]) -> None:
    assert context["runner"].processes[-1].killed.is_set()


@then("the page says the map server is not running")
def says_not_running(context: dict[str, Any]) -> None:
    assert "The map server is not running." in _text(context)


@then("the page says the map server stopped with an error")
def says_failed(context: dict[str, Any]) -> None:
    assert "The map server stopped with an error" in _text(context)


@then(parsers.parse('the page shows "{text}"'))
def page_shows(context: dict[str, Any], text: str) -> None:
    assert text in _text(context)


@then(parsers.parse('the MCP configuration runs "{args}" with this Python'))
def mcp_runs(context: dict[str, Any], args: str) -> None:
    server = _mcp_config(context)
    assert server["command"] == sys.executable
    assert server["args"] == args.split()


@then(
    "the MCP configuration sets SPOOR_CACHE_DIR to this GUI's cache folder "
    "as an absolute path"
)
def mcp_cache(context: dict[str, Any]) -> None:
    value = _mcp_config(context)["env"]["SPOOR_CACHE_DIR"]
    assert os.path.isabs(value)
    assert value == os.path.abspath(context["workdir"] / ".spoor-cache")


@then("the page shows the claude mcp add command for the same server")
def claude_command(context: dict[str, Any]) -> None:
    text = html.unescape(_text(context))
    assert "claude mcp add spoor --env SPOOR_CACHE_DIR=" in text
    assert "-m spoor.cli serve-mcp" in text


@then(parsers.parse('the MCP server lists the mapped site "{domain}"'))
def mcp_lists(context: dict[str, Any], domain: str) -> None:
    assert domain in context["mcp_answer"], context["mcp_answer"]


@then("its local cache is that folder")
def cache_is_folder(context: dict[str, Any]) -> None:
    assert context["cache_seen"] == context["expected_cache"]


@then(parsers.parse('its local cache is "{name}" in the working folder'))
def cache_default(context: dict[str, Any], name: str) -> None:
    assert context["cache_seen"] == os.path.abspath(context["cwd"] / name)


@then("the browser shows the map server running")
def browser_running(context: dict[str, Any]) -> None:
    url = f"http://127.0.0.1:{context['serve_port']}"
    assert url in context["page"].inner_text("main")


@then(parsers.parse('the running server lists the mapped site "{domain}"'))
def server_lists(context: dict[str, Any], domain: str) -> None:
    response = httpx.get(f"http://127.0.0.1:{context['serve_port']}/domains")
    assert domain in response.json()["domains"]


@then("the server no longer answers")
def server_gone(context: dict[str, Any]) -> None:
    with pytest.raises(httpx.HTTPError):
        httpx.get(f"http://127.0.0.1:{context['serve_port']}/healthz", timeout=2)
