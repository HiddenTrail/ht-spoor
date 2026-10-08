"""Unit tests for the local GUI's helpers (ROADMAP.md §2i).

The behaviour-level contract lives in features/gui.feature; these pin the small
boundaries the scenarios don't reach directly.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from spoor.gui.app import create_app, human_age, token_cookie
from spoor.gui.launch import GuiError, start_gui
from spoor.security import storage
from spoor.serving.store import MapStore


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (-5, "just now"),
        (0, "just now"),
        (59, "just now"),
        (60, "1 minute ago"),
        (119, "1 minute ago"),
        (3600, "1 hour ago"),
        (7200, "2 hours ago"),
        (86399, "23 hours ago"),
        (86400, "1 day ago"),
        (10 * 86400, "10 days ago"),
    ],
)
def test_human_age_boundaries(seconds: float, expected: str) -> None:
    assert human_age(seconds) == expected


@pytest.mark.parametrize(
    "host", ["0.0.0.0", "::", "192.168.1.5", "localhost.evil.example", ""]
)
def test_launcher_refuses_every_non_loopback_host(host: str) -> None:
    with pytest.raises(GuiError, match="local-only"):
        start_gui(MapStore(), host=host)


def test_a_same_origin_post_passes_the_guard(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The guard lets this GUI's own origin through (405: no POST route exists in
    # gui-1), so the 403 in the cross-site scenario really is the Origin check.
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path)
    app = create_app(MapStore(), token="t", port=9000)
    client = TestClient(app, base_url="http://127.0.0.1:9000")
    client.cookies.set(token_cookie(9000), "t")
    response = client.post("/", headers={"origin": "http://127.0.0.1:9000"})
    assert response.status_code == 405


def test_a_non_ascii_token_is_rejected_not_crashed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path)
    app = create_app(MapStore(), token="t", port=9000)
    client = TestClient(app, base_url="http://127.0.0.1:9000")
    response = client.get("/launch", params={"token": "tö"})
    assert response.status_code == 403


def test_a_gui_on_another_loopback_address_accepts_its_own_host(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Any 127.x address is loopback, so the launcher allows it; the app must then
    # accept requests addressed to that same address, not only 127.0.0.1.
    import httpx

    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path)
    gui = start_gui(MapStore(), host="127.0.0.2")
    try:
        response = httpx.get(gui.launch_url, follow_redirects=True)
        assert response.status_code == 200
        assert "Nothing has been mapped yet" in response.text
    finally:
        gui.stop()


def test_closing_the_gui_stops_its_running_jobs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # An unsupervised browser left running after the GUI closes is exactly what
    # §2i gui-2 rules out, so stopping the server must shut the job manager down.
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path)
    gui = start_gui(MapStore(), workdir=tmp_path)
    calls: list[str] = []
    monkeypatch.setattr(gui._jobs, "shutdown", lambda: calls.append("shutdown"))
    gui.stop()
    assert calls == ["shutdown"]


def test_a_clean_exit_that_beats_a_force_stop_is_reported_as_finished(
    tmp_path: Path,
) -> None:
    # Force stop pressed just as the command exits cleanly on its own: the run
    # did finish, so it must not be labelled as stopped.
    from spoor.gui.commands import CommandSpec
    from spoor.gui.jobs import Job, JobManager

    manager = JobManager(runner=None, workdir=tmp_path)  # type: ignore[arg-type]
    job = Job("j1", CommandSpec("explore", ["explore", "x"]), tmp_path / "s")
    job.killed = True
    manager._finish(job, 0)
    assert job.status == "succeeded"
    killed = Job("j2", CommandSpec("explore", ["explore", "x"]), tmp_path / "s")
    killed.killed = True
    manager._finish(killed, 1)
    assert killed.status == "stopped"


def test_a_carriage_return_never_splits_a_log_line(tmp_path: Path) -> None:
    from spoor.gui.commands import CommandSpec
    from spoor.gui.jobs import Job, JobManager

    manager = JobManager(runner=None, workdir=tmp_path)  # type: ignore[arg-type]
    job = Job("j1", CommandSpec("run", ["run", "x"]), tmp_path / "s")
    manager._append(job, "[###--] 50%\rprogress: 3 state(s)")
    assert job.lines_from(0) == (1, ["[###--] 50%progress: 3 state(s)"])


def test_shutdown_removes_the_stop_file_folder(tmp_path: Path) -> None:
    from spoor.gui.jobs import JobManager

    class Instant:
        def start(self, args: object, env: dict[str, str]) -> object:
            class Done:
                def readline(self) -> str:
                    return ""

                def wait(self) -> int:
                    return 0

                def kill(self) -> None:
                    pass

            return Done()

    from spoor.gui.commands import CommandSpec

    manager = JobManager(Instant(), tmp_path)  # type: ignore[arg-type]
    job = manager.start(CommandSpec("explore", ["explore", "x"]))
    stop_dir = job.stop_file.parent
    assert stop_dir.is_dir()
    manager.shutdown()
    assert not stop_dir.exists()


def test_describe_changes_lists_only_what_changed_in_plain_words() -> None:
    from spoor.gui.app import describe_changes

    assert describe_changes(
        {
            "ax_node_delta": 4,
            "console_added": ["auth header Bearer [REDACTED]"],
            "storage_added": ["cartId", "theme"],
            "storage_removed": [],
            "screenshot_changed": True,
        }
    ) == [
        "accessibility nodes: +4",
        "console added: auth header Bearer [REDACTED]",
        "storage added: cartId, theme",
        "screenshot changed",
    ]
    assert describe_changes({"ax_node_delta": 0, "screenshot_changed": False}) == [
        "nothing observed"
    ]
    assert describe_changes(None) == []


def _config_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    from spoor.gui.jobs import JobManager

    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / ".spoor-cache")
    jobs = JobManager(runner=None, workdir=tmp_path)  # type: ignore[arg-type]
    app = create_app(MapStore(), token="t", port=9000, jobs=jobs)
    client = TestClient(app, base_url="http://127.0.0.1:9000")
    client.cookies.set(token_cookie(9000), "t")
    return client


@pytest.mark.parametrize(
    ("content", "reason"),
    [
        (b"target: x\n" + b"#" * 1_000_001, "too large"),
        (b"target: caf\xe9\n", "UTF-8"),
    ],
    ids=["too-large", "not-utf8"],
)
def test_a_config_that_cant_be_edited_safely_gets_no_editor(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, content: bytes, reason: str
) -> None:
    # An empty editor with a Save button would let one click wipe or corrupt the
    # file, so no editor (and no Save) is offered at all.
    (tmp_path / "big.yaml").write_bytes(content)
    response = _config_client(tmp_path, monkeypatch).get(
        "/configs/edit", params={"path": "big.yaml"}
    )
    assert response.status_code == 400
    assert reason in response.text
    assert "/configs/save" not in response.text
    assert (tmp_path / "big.yaml").read_bytes() == content


def test_saving_onto_a_folder_is_refused_not_a_crash(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "odd.yaml").mkdir()
    response = _config_client(tmp_path, monkeypatch).post(
        "/configs/save",
        data={"path": "odd.yaml", "text": "target: x\n"},
        headers={"origin": "http://127.0.0.1:9000"},
    )
    assert response.status_code == 404


def test_a_symlink_out_of_the_working_folder_is_not_listed(tmp_path: Path) -> None:
    from spoor.gui import configs

    work = tmp_path / "work"
    work.mkdir()
    outside = tmp_path / "outside.yaml"
    outside.write_text("target: x\n", encoding="utf-8")
    (work / "inside.yaml").write_text("target: x\n", encoding="utf-8")
    try:
        (work / "link.yaml").symlink_to(outside)
    except OSError:
        pytest.skip("creating symlinks isn't permitted here")
    assert [c.path for c in configs.find(work)] == ["inside.yaml"]


def test_config_check_reports_where_each_problem_is() -> None:
    from spoor.gui import configs

    valid = "target: https://x.example/\nfields:\n  title: { selector: h2 }\n"
    assert configs.check(valid) == []
    assert configs.check("target: https://x.example/\n") == ["fields: Field required"]
    # A new config starts from the starter, which must itself be valid.
    assert configs.check(configs.STARTER) == []
    yaml_problem = configs.check("target: [unclosed\n")
    assert len(yaml_problem) == 1 and "line 2" in yaml_problem[0]
    assert configs.check("")[0].startswith("the whole file:")


@pytest.mark.parametrize(
    ("existing", "expected"),
    [
        (b"target: x\r\nfields: {}\r\n", b"target: y\r\nfields: {}\r\n"),
        (b"target: x\nfields: {}\n", b"target: y\nfields: {}\n"),
        (None, b"target: y\nfields: {}\n"),
    ],
    ids=["keeps-crlf", "keeps-lf", "new-file-lf"],
)
def test_saving_keeps_the_files_line_break_style(
    tmp_path: Path, existing: bytes | None, expected: bytes
) -> None:
    # A browser submits CRLF whatever the file used; saving must not rewrite
    # every line ending of a file that wasn't really changed.
    from spoor.gui import configs

    path = tmp_path / "c.yaml"
    if existing is not None:
        path.write_bytes(existing)
    configs.write(path, "target: y\r\nfields: {}\r\n")
    assert path.read_bytes() == expected


def test_the_guis_logo_is_the_brand_file_unchanged() -> None:
    # The GUI ships its own copy (docs/ isn't packaged); it must never drift from
    # the canonical brand file in docs/assets/.
    import base64

    from spoor.gui.templates import logo_data_uri

    root = Path(__file__).resolve().parent.parent
    brand = (root / "docs" / "assets" / "Spoor_O_B.svg").read_bytes()
    shipped = (root / "spoor" / "gui" / "assets" / "spoor-logo.svg").read_bytes()
    assert shipped == brand
    prefix = "data:image/svg+xml;base64,"
    assert logo_data_uri() == prefix + base64.b64encode(brand).decode("ascii")
