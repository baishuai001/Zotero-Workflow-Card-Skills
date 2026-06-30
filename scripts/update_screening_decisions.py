#!/usr/bin/env python3
"""Upsert one paper row into screening_decisions.csv."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


COLUMNS = [
    "paper_id",
    "title",
    "doi",
    "zotero_item_key",
    "screening_status",
    "decision_reason",
    "needs_full_text",
    "notes",
]


def row_key(row: dict[str, str]) -> tuple[str, str]:
    for key in ("doi", "zotero_item_key", "paper_id", "title"):
        value = (row.get(key) or "").strip().lower()
        if value:
            return key, value
    raise SystemExit("Row needs at least one of doi, zotero_item_key, paper_id, or title")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default="./workflow_cards")
    parser.add_argument("--row-json", required=True)
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    screening = root / "screening_decisions.csv"
    root.mkdir(parents=True, exist_ok=True)

    new_row_raw = json.loads(Path(args.row_json).read_text(encoding="utf-8-sig"))
    new_row = {column: str(new_row_raw.get(column, "")) for column in COLUMNS}
    match_key, match_value = row_key(new_row)

    rows: list[dict[str, str]] = []
    updated = False
    if screening.exists():
        with screening.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                normalized = {column: row.get(column, "") for column in COLUMNS}
                if (normalized.get(match_key) or "").strip().lower() == match_value:
                    rows.append(new_row)
                    updated = True
                else:
                    rows.append(normalized)

    if not updated:
        rows.append(new_row)

    with screening.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"{'Updated' if updated else 'Added'} row in {screening.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
