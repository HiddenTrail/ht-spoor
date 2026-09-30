"""Output pipeline: pluggable, schema-validated sinks (ROADMAP.md §2d).

Downstream of extraction: take the records a run produced and write them in a
chosen format. Per §2d the field schema from §2a is validated (via pydantic)
*before* anything is written, so a stray or mistyped field fails loudly instead
of landing silently in the output. An output file is a shared surface, so per
§2h known secret shapes in record values are redacted (default-on) before any
write. Per §0 there is nothing site-specific here — the schema is derived from
the config, whatever the target.

Phase-1 formats are the dependency-free text sinks (JSON, JSON Lines, CSV,
Markdown). SQLite and Parquet are named in §2d as further sinks and land later.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Literal, cast, get_args

from pydantic import BaseModel, ConfigDict, create_model

from spoor.core.config import ExtractionConfig
from spoor.security.redaction import redact_records

OutputFormat = Literal["json", "jsonl", "csv", "md"]

_BY_SUFFIX: dict[str, OutputFormat] = {
    ".json": "json",
    ".jsonl": "jsonl",
    ".csv": "csv",
    ".md": "md",
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
    else:  # md
        _write_markdown(records=rows, config=config, path=path)


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
