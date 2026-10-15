"""Read the historical snapshot without altering it or silently inventing columns."""

import hashlib
import re
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd

TABLE_PATTERN = re.compile(r"crime_(\d{4})_([12])\Z")


def parse_date(value):
    """Preserve the source calendar date; offset conventions differ across tables.

    The city defines 2023 DATEEND as date reported; earlier semantics and
    publication timing remain unverified. Never convert mixed
    midnight conventions to New York time, which would shift some dates backward.
    """
    if not isinstance(value, str) or not value.strip():
        return pd.NaT
    token = value.strip().split()[0]
    for fmt in ("%Y/%m/%d", "%m/%d/%Y", "%Y-%m-%d"):
        try:
            return pd.Timestamp(datetime.strptime(token, fmt))
        except ValueError:
            continue
    return pd.NaT


def load_records(database, start="2020-01-01", end="2024-12-31"):
    """Return date/category records and a reconciliation audit, never addresses.

    Include source-year tables intersecting the requested window. Keep repeated
    date/category pairs: they can represent distinct records. IDs are table-local
    and do not establish a cross-table incident identity.
    """
    path = Path(database).expanduser().resolve(strict=True)
    start, end = pd.Timestamp(start).normalize(), pd.Timestamp(end).normalize()
    if pd.isna(start) or pd.isna(end) or start > end:
        raise ValueError("start and end must define a valid date window")
    frames, tables, skipped = [], [], []
    with sqlite3.connect(path.as_uri() + "?mode=ro", uri=True) as conn:
        names = [row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )]
        for table in names:
            match = TABLE_PATTERN.fullmatch(table)
            if not match or not start.year <= int(match[1]) <= end.year:
                skipped.append(table)
                continue
            columns = {row[1] for row in conn.execute(f'PRAGMA table_info("{table}")')}
            label = next((c for c in ("CODE_DEFINED", "CODE DEFINED") if c in columns), None)
            if "DATEEND" not in columns or label is None:
                raise ValueError(f"{table}: missing DATEEND or crime-category column")
            raw = pd.read_sql_query(
                f'SELECT DATEEND AS raw_date, "{label}" AS category FROM "{table}"', conn
            )
            dates = raw.raw_date.map(parse_date)
            labels = raw.category.astype("string").str.strip().str.upper()
            invalid_date = dates.isna()
            invalid_label = ~invalid_date & (labels.isna() | labels.eq(""))
            outside = ~invalid_date & ~invalid_label & ~dates.between(start, end)
            keep = ~(invalid_date | invalid_label | outside)
            frame = pd.DataFrame({"date": dates[keep], "category": labels[keep]})
            frame["source_table"] = table
            frames.append(frame)
            tables.append({
                "table": table, "label_column": label, "raw_rows": len(raw),
                "invalid_date": int(invalid_date.sum()),
                "missing_category": int(invalid_label.sum()),
                "outside_window": int(outside.sum()), "retained_rows": len(frame),
                "first_date": str(frame.date.min().date()) if len(frame) else None,
                "last_date": str(frame.date.max().date()) if len(frame) else None,
            })
    if not frames or not sum(len(frame) for frame in frames):
        raise ValueError("No usable crime records in the requested source tables/date window")
    records = pd.concat(frames, ignore_index=True).sort_values("date", kind="stable")
    records.reset_index(drop=True, inplace=True)
    audit = {
        "database_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "requested_start": str(start.date()), "requested_end": str(end.date()),
        "raw_rows": sum(t["raw_rows"] for t in tables), "retained_rows": len(records),
        "excluded_rows": sum(t["raw_rows"] - t["retained_rows"] for t in tables),
        "tables": tables, "skipped_tables": skipped,
        "date_policy": "Preserve the calendar date written in DATEEND; no timezone conversion.",
        "unit": "Source records, not verified unique incidents or population-adjusted rates.",
        "duplicate_policy": "Retain records; no stable cross-table incident identifier.",
    }
    return records, audit
