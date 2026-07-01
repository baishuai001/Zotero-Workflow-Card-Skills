#!/usr/bin/env python3
"""Finalize one Workflow Card and keep project tracking files in sync."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


MATRIX_COLUMNS = [
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


SCREENING_COLUMNS = [
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


def safe_slug(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", text.strip()).strip("-")
    return slug or "workflow-card"


def load_json(path: str | None) -> dict[str, str]:
    if not path:
        return {}
    payload = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise SystemExit(f"JSON file must contain an object: {path}")
    return {str(key): "" if value is None else str(value) for key, value in payload.items()}


def row_key(row: dict[str, str], keys: tuple[str, ...]) -> tuple[str, str]:
    for key in keys:
        value = (row.get(key) or "").strip().lower()
        if value:
            return key, value
    raise SystemExit(f"Row needs at least one identity field: {', '.join(keys)}")


def read_rows(path: Path, columns: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [{column: row.get(column, "") for column in columns} for row in reader]


def write_rows(path: Path, columns: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def upsert_replace(
    path: Path,
    columns: list[str],
    new_row: dict[str, str],
    identity_keys: tuple[str, ...],
) -> bool:
    match_key, match_value = row_key(new_row, identity_keys)
    rows = read_rows(path, columns)
    output: list[dict[str, str]] = []
    updated = False
    for row in rows:
        if (row.get(match_key) or "").strip().lower() == match_value:
            output.append({column: new_row.get(column, "") for column in columns})
            updated = True
        else:
            output.append(row)
    if not updated:
        output.append({column: new_row.get(column, "") for column in columns})
    write_rows(path, columns, output)
    return updated


def upsert_merge(
    path: Path,
    columns: list[str],
    new_row: dict[str, str],
    identity_keys: tuple[str, ...],
) -> bool:
    match_key, match_value = row_key(new_row, identity_keys)
    rows = read_rows(path, columns)
    output: list[dict[str, str]] = []
    updated = False
    for row in rows:
        if (row.get(match_key) or "").strip().lower() == match_value:
            merged = dict(row)
            for column, value in new_row.items():
                if value:
                    merged[column] = value
            output.append({column: merged.get(column, "") for column in columns})
            updated = True
        else:
            output.append(row)
    if not updated:
        output.append({column: new_row.get(column, "") for column in columns})
    write_rows(path, columns, output)
    return updated


def run_validation(project_root: Path) -> None:
    script = Path(__file__).resolve().parent / "validate_project.py"
    result = subprocess.run(
        [sys.executable, str(script), "--project-root", str(project_root)],
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default="./workflow_cards")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--content-file", required=True)
    parser.add_argument("--row-json", required=True, help="Workflow Matrix row JSON")
    parser.add_argument("--screening-row-json", help="Optional screening row fields to merge")
    parser.add_argument("--screening-status", default="full-card")
    parser.add_argument("--workflow-card-status", default="matrix-updated")
    parser.add_argument("--action-next", default="hold")
    parser.add_argument("--skip-validate", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    cards = root / "cards"
    cards.mkdir(parents=True, exist_ok=True)

    slug = safe_slug(args.slug)
    card = cards / f"{slug}.md"
    card.write_text(Path(args.content_file).read_text(encoding="utf-8").rstrip() + "\n", encoding="utf-8")
    card_path = str(PurePosixPath("cards") / f"{slug}.md")

    matrix_raw = load_json(args.row_json)
    screening_raw = load_json(args.screening_row_json)

    matrix_row = {column: matrix_raw.get(column, "") for column in MATRIX_COLUMNS}
    matrix_row["card_path"] = card_path
    matrix_row["screening_status"] = args.screening_status

    screening_row = {column: "" for column in SCREENING_COLUMNS}
    for column in SCREENING_COLUMNS:
        if column in matrix_raw:
            screening_row[column] = matrix_raw[column]
    for column, value in screening_raw.items():
        if column in screening_row and value:
            screening_row[column] = value
    screening_row["card_path"] = card_path
    screening_row["screening_status"] = args.screening_status
    screening_row["workflow_card_status"] = args.workflow_card_status
    screening_row["action_next"] = args.action_next
    if not screening_row.get("inclusion_decision"):
        screening_row["inclusion_decision"] = "include"
    if not screening_row.get("needs_full_text"):
        screening_row["needs_full_text"] = "no"
    if not screening_row.get("decision_reason"):
        screening_row["decision_reason"] = "Finalized Workflow Card and updated Workflow Matrix"

    matrix_updated = upsert_replace(
        root / "workflow_matrix.csv",
        MATRIX_COLUMNS,
        matrix_row,
        ("doi", "zotero_item_key", "paper_id", "title"),
    )
    screening_updated = upsert_merge(
        root / "screening_decisions.csv",
        SCREENING_COLUMNS,
        screening_row,
        ("doi", "pmid", "zotero_item_key", "paper_id", "screening_id", "title"),
    )

    if not args.skip_validate:
        run_validation(root)

    print(f"Workflow Card: {card.resolve()}")
    print(f"Workflow Matrix: {root / 'workflow_matrix.csv'} ({'updated' if matrix_updated else 'added'})")
    print(f"Screening decisions: {root / 'screening_decisions.csv'} ({'updated' if screening_updated else 'added'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
