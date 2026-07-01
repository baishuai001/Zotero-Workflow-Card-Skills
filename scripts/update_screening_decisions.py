#!/usr/bin/env python3
"""Upsert one paper row into screening_decisions.csv."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


COLUMNS = [
    "screening_id",
    "search_round",
    "query_id",
    "source_database",
    "search_query",
    "retrieved_date",
    "paper_id",
    "title",
    "year",
    "journal",
    "doi",
    "pmid",
    "url",
    "authors",
    "abstract_available",
    "full_text_available",
    "zotero_target_collection",
    "zotero_item_key",
    "bibtex_key",
    "zotero_status",
    "topic_fit",
    "workflow_relevance",
    "data_relevance",
    "public_data_relevance",
    "method_signal",
    "study_scope",
    "cell_type",
    "cancer_type",
    "data_type",
    "workflow_type_hint",
    "inclusion_decision",
    "exclusion_reason",
    "duplicate_of",
    "decision_reason",
    "screening_status",
    "priority",
    "design_sample_role",
    "needs_full_text",
    "action_next",
    "reviewer",
    "workflow_card_status",
    "card_path",
    "notes",
]


def row_key(row: dict[str, str]) -> tuple[str, str]:
    for key in ("doi", "pmid", "zotero_item_key", "paper_id", "screening_id", "title"):
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
                    merged = dict(normalized)
                    for column, value in new_row.items():
                        if value:
                            merged[column] = value
                    rows.append(merged)
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
