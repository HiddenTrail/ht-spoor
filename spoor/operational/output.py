"""Output pipeline: pluggable, schema-validated sinks (ROADMAP.md §2d).

Downstream of extraction: take the records a run produced and write them in a
chosen format. Per §2d the field schema from §2a is validated (via pydantic)
*before* anything is written, so a stray or mistyped field fails loudly instead
of landing silently in the output. An output file is a shared surface, so per
§2h known secret shapes in record values are redacted (default-on) before any
write. Per §0 there is nothing site-specific here — the schema is derived from
the config, whatever the target.

Phase-1 shipped the dependency-free text sinks (JSON, JSON Lines, CSV,
Markdown). SQLite (stdlib `sqlite3`) and Parquet (optional `pyarrow` extra,
`pip install 'ht-spoor[parquet]'`) round out the §2d sink list; both still go
through the same validate-before-write and redact-before-write pipeline as
every other format, a plain table of the config's fields in declared order.
"""

from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path
from typing import Any, Literal, cast, get_args

from pydantic import BaseModel, ConfigDict, create_model

from spoor.core.config import ExtractionConfig
from spoor.security.redaction import redact_records

OutputFormat = Literal["json", "jsonl", "csv", "md", "sqlite", "parquet"]

_BY_SUFFIX: dict[str, OutputFormat] = {
    ".json": "json",
    ".jsonl": "jsonl",
    ".csv": "csv",
    ".md": "md",
    ".sqlite": "sqlite",
    ".parquet": "parquet",
}


def resolve_format(path: Path, explicit: str | None) -> OutputFormat:
    """Pick the output format: an explicit choice wins, else infer from suffix.

    Raises ValueError (before any write) on an unknown explicit format or a file
    extension we can't map to one.
    """
    choices = get_args(OutputFormat)
    if explicit is not None:
        if explicit not in choices:
            raise ValueError(
                f"unknown output format {explicit!r}; choose from {', '.join(choices)}"
            )
        return cast(OutputFormat, explicit)
    fmt = _BY_SUFFIX.get(path.suffix.lower())
    if fmt is None:
        raise ValueError(
            f"cannot infer output format from {path.name!r}; "
            f"pass --format ({', '.join(choices)})"
        )
    return fmt


def _row_model(config: ExtractionConfig) -> type[BaseModel]:
    """A strict pydantic model for one output row, built from the config fields."""
    fields: dict[str, Any] = {}
    for name, spec in config.fields.items():
        annotation = float | None if spec.type == "number" else str | None
        # `...` = required: every declared field must be present (value may be
        # null); `extra="forbid"` rejects any field not in the config schema.
        fields[name] = (annotation, ...)
    return create_model(
        "OutputRow",
        __config__=ConfigDict(extra="forbid"),
        **fields,
    )


def _validated_rows(
    records: list[dict[str, object]], config: ExtractionConfig
) -> list[dict[str, object]]:
    model = _row_model(config)
    # Validate every record before opening the output file, so a schema
    # violation aborts the whole write rather than leaving a partial file.
    return [model.model_validate(record).model_dump() for record in records]


def write_records(
    records: list[dict[str, object]],
    config: ExtractionConfig,
    path: Path,
    fmt: OutputFormat,
) -> None:
    """Validate `records` against the config schema, then write them as `fmt`.

    An output file is a shared surface, so records pass through secret redaction
    (§2h) after validation and before any write — on by default, no opt-out here.
    The raw records remain only in the local-only cache/map; only this redacted
    form reaches the file.
    """
    rows = redact_records(_validated_rows(records, config))
    if fmt == "json":
        path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    elif fmt == "jsonl":
        body = "".join(json.dumps(row) + "\n" for row in rows)
        path.write_text(body, encoding="utf-8")
    elif fmt == "csv":
        _write_csv(records=rows, config=config, path=path)
    elif fmt == "md":
        _write_markdown(records=rows, config=config, path=path)
    elif fmt == "sqlite":
        _write_sqlite(records=rows, config=config, path=path)
    else:  # parquet
        _write_parquet(records=rows, config=config, path=path)


def _write_csv(
    records: list[dict[str, object]], config: ExtractionConfig, path: Path
) -> None:
    fieldnames = list(config.fields)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in records:
            writer.writerow(
                {key: "" if value is None else value for key, value in row.items()}
            )


def _md_cell(value: object) -> str:
    """One Markdown table cell's text: escaped so it can never break the row.

    A raw `|` would be read as a new column boundary and a raw newline as a new
    row, so both are neutralized here rather than left to corrupt the table —
    the same "never let a captured value break the format" posture CSV's quoting
    already gives it for free via the stdlib `csv` module. `None` renders as an
    empty cell, matching CSV's empty-cell convention for a missing field.
    """
    if value is None:
        return ""
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def _write_markdown(
    records: list[dict[str, object]], config: ExtractionConfig, path: Path
) -> None:
    fieldnames = list(config.fields)
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join("---" for _ in fieldnames) + " |"
    lines = [header, separator]
    for row in records:
        cells = " | ".join(_md_cell(row.get(name)) for name in fieldnames)
        lines.append(f"| {cells} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_sqlite(
    records: list[dict[str, object]], config: ExtractionConfig, path: Path
) -> None:
    # A fresh file each write, like every other sink: re-running against the
    # same path replaces its contents rather than erroring on a pre-existing
    # "records" table or silently appending to a stale one.
    path.unlink(missing_ok=True)
    fieldnames = list(config.fields)
    columns = ", ".join(
        f'"{name}" {"REAL" if config.fields[name].type == "number" else "TEXT"}'
        for name in fieldnames
    )
    placeholders = ", ".join("?" for _ in fieldnames)
    quoted_names = ", ".join(f'"{name}"' for name in fieldnames)
    # sqlite3.Connection used as a context manager commits/rolls back the
    # transaction but does *not* close the connection, which leaves the file
    # handle open (and, on Windows, the file locked against a later write to
    # the same path) — closed explicitly here instead.
    conn = sqlite3.connect(path)
    try:
        conn.execute(f"CREATE TABLE records ({columns})")
        conn.executemany(
            f"INSERT INTO records ({quoted_names}) VALUES ({placeholders})",
            [tuple(row.get(name) for name in fieldnames) for row in records],
        )
        conn.commit()
    finally:
        conn.close()


def _write_parquet(
    records: list[dict[str, object]], config: ExtractionConfig, path: Path
) -> None:
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except ImportError as exc:
        raise ImportError(
            "Parquet output requires pyarrow; install with "
            "pip install 'ht-spoor[parquet]'"
        ) from exc
    fieldnames = list(config.fields)
    pa_type = {
        name: pa.float64() if config.fields[name].type == "number" else pa.string()
        for name in fieldnames
    }
    columns = {
        name: pa.array([row.get(name) for row in records], type=pa_type[name])
        for name in fieldnames
    }
    table = pa.table(columns)
    pq.write_table(table, path)
