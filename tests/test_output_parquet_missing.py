"""Unit test for the Parquet sink's missing-dependency path (ROADMAP.md §2d).

Parquet needs the optional `pyarrow` extra; every other scenario in
`output.feature` runs with it installed (it's a `dev` dependency, since the
feature scenarios need it too), so the one thing worth proving here — a clean,
pre-write error when it's absent — can't be driven through a real missing
install. `builtins.__import__` is patched instead, scoped to just the `pyarrow`
imports `_write_parquet` makes, so the rest of the test run is unaffected.
"""

from __future__ import annotations

import builtins
from pathlib import Path
from typing import Any

import pytest

from spoor.core.config import load_config
from spoor.operational import output

_CONFIG_TEXT = """
target: http://localhost:8000/x.html
fields:
  title: { selector: "h1" }
"""


def test_parquet_without_pyarrow_fails_before_writing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    real_import = builtins.__import__

    def fake_import(name: str, *args: Any, **kwargs: Any) -> Any:
        if name == "pyarrow" or name.startswith("pyarrow."):
            raise ImportError(f"No module named {name!r}")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    cfg = load_config(_CONFIG_TEXT)
    path = tmp_path / "out.parquet"
    with pytest.raises(ImportError, match="pip install 'ht-spoor\\[parquet\\]'"):
        output.write_records([{"title": "Mug"}], cfg, path, "parquet")
    assert not path.exists()
