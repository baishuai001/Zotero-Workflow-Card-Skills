#!/usr/bin/env python3
"""Validate a Zotero Workflow Card project."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


SCREENING_REQUIRED_COLUMNS = [
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


MATRIX_REQUIRED_COLUMNS = [
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


ALLOWED_SCREENING_STATUS = {
    "candidate",
    "title-abstract-screened",
    "included-for-full-text",
    "excluded",
    "needs-full-text",
    "ready-for-workflow-card",
    "partial-card",
    "full-card",
    "duplicate",
    "hold",
}

ALLOWED_DESIGN_SAMPLE_ROLE = {
    "",
    "pending",
    "canonical-example",
    "contrast-case",
    "counterexample",
    "gap-filler",
    "method-reference",
    "validation-reference",
}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def row_label(row: dict[str, str], index: int) -> str:
    return (
        row.get("paper_id")
        or row.get("zotero_item_key")
        or row.get("doi")
        or row.get("title")
        or f"row-{index + 1}"
    )


def normalized(value: str | None) -> str:
    return (value or "").strip().lower()


def split_roles(value: str | None) -> list[str]:
    text = (value or "").strip()
    if not text:
        return [""]
    return [part.strip() for part in text.split(";") if part.strip()]


def resolve_card_path(project_root: Path, value: str | None) -> Path | None:
    text = (value or "").strip()
    if not text:
        return None
    path = Path(text)
    if path.is_absolute():
        return path
    return project_root / path


def add_missing_column_errors(
    path: Path,
    actual_columns: list[str],
    required_columns: list[str],
    errors: list[str],
) -> None:
    if not actual_columns:
        errors.append(f"Missing CSV file or header: {path}")
        return
    missing = [column for column in required_columns if column not in actual_columns]
    if missing:
        errors.append(f"{path.name} missing required columns: {', '.join(missing)}")


def duplicate_errors(rows: list[dict[str, str]], field: str) -> list[str]:
    seen: dict[str, list[str]] = defaultdict(list)
    for index, row in enumerate(rows):
        value = normalized(row.get(field))
        if value:
            seen[value].append(row_label(row, index))
    errors = []
    for value, labels in seen.items():
        if len(labels) > 1:
            errors.append(f"Duplicate {field}={value}: {', '.join(labels)}")
    return errors


def row_identity(row: dict[str, str]) -> tuple[str, str] | None:
    for field in ("doi", "pmid", "zotero_item_key", "paper_id", "title"):
        value = normalized(row.get(field))
        if value:
            return field, value
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default="./workflow_cards")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    screening_path = project_root / "screening_decisions.csv"
    matrix_path = project_root / "workflow_matrix.csv"

    errors: list[str] = []
    warnings: list[str] = []

    screening_columns, screening_rows = read_csv(screening_path)
    matrix_columns, matrix_rows = read_csv(matrix_path)

    add_missing_column_errors(screening_path, screening_columns, SCREENING_REQUIRED_COLUMNS, errors)
    add_missing_column_errors(matrix_path, matrix_columns, MATRIX_REQUIRED_COLUMNS, errors)

    for field in ("doi", "pmid", "zotero_item_key"):
        errors.extend(duplicate_errors(screening_rows, field))

    for index, row in enumerate(screening_rows):
        label = row_label(row, index)
        status = (row.get("screening_status") or "").strip()
        if status and status not in ALLOWED_SCREENING_STATUS:
            errors.append(f"{label}: invalid screening_status={status}")
        for role in split_roles(row.get("design_sample_role")):
            if role not in ALLOWED_DESIGN_SAMPLE_ROLE:
                errors.append(f"{label}: invalid design_sample_role={role}")
        if status == "full-card":
            card_path = resolve_card_path(project_root, row.get("card_path"))
            if not card_path:
                errors.append(f"{label}: full-card row missing card_path")
            elif not card_path.exists():
                errors.append(f"{label}: card_path does not exist: {card_path}")
        if status == "ready-for-workflow-card" and not (row.get("card_path") or "").strip():
            warnings.append(f"{label}: ready-for-workflow-card but no card_path yet")

    screening_identities = {row_identity(row) for row in screening_rows}
    screening_identities.discard(None)

    for index, row in enumerate(matrix_rows):
        label = row_label(row, index)
        status = (row.get("screening_status") or "").strip()
        if status and status not in ALLOWED_SCREENING_STATUS:
            errors.append(f"{label}: invalid matrix screening_status={status}")
        for role in split_roles(row.get("design_sample_role")):
            if role not in ALLOWED_DESIGN_SAMPLE_ROLE:
                errors.append(f"{label}: invalid matrix design_sample_role={role}")
        card_path = resolve_card_path(project_root, row.get("card_path"))
        if row.get("card_path") and card_path and not card_path.exists():
            errors.append(f"{label}: matrix card_path does not exist: {card_path}")
        identity = row_identity(row)
        if identity and identity not in screening_identities:
            warnings.append(f"{label}: matrix row has no matching screening row by DOI/PMID/Zotero key/paper_id/title")

    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"- {error}")
        return 1
    if warnings and args.strict:
        return 1
    print(f"Validation passed: {len(screening_rows)} screening rows, {len(matrix_rows)} matrix rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
