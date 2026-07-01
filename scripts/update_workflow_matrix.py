#!/usr/bin/env python3
"""Upsert one paper row into workflow_matrix.csv."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


COLUMNS = [
    "paper_id",
    "title",
    "year",
    "journal",
    "doi",
    "pmid",
    "zotero_item_key",
    "bibtex_key",
    "cell_type",
    "cancer_type",
    "data_type",
    "core_question",
    "main_claims",
    "data_credibility_basis",
    "cell_identity_basis",
    "conclusion_evidence_basis",
    "data_supports_workflow",
    "main_workflow_type",
    "workflow_trunk",
    "downstream_modules",
    "evidence_chain",
    "key_technical_choices",
    "workflow_rationale",
    "counterfactual_risk",
    "public_data_strategy",
    "reusable_design_principle",
    "limitations",
    "screening_status",
    "priority",
    "design_sample_role",
    "card_path",
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
    matrix = root / "workflow_matrix.csv"
    root.mkdir(parents=True, exist_ok=True)

    new_row_raw = json.loads(Path(args.row_json).read_text(encoding="utf-8-sig"))
    new_row = {column: str(new_row_raw.get(column, "")) for column in COLUMNS}
    match_key, match_value = row_key(new_row)

    rows: list[dict[str, str]] = []
    updated = False
    if matrix.exists():
        with matrix.open("r", newline="", encoding="utf-8") as handle:
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

    with matrix.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"{'Updated' if updated else 'Added'} row in {matrix.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
