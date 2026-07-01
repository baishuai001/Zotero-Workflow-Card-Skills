#!/usr/bin/env python3
"""Initialize a Zotero Workflow Card project."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


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


def write_csv_if_missing(path: Path, columns: list[str]) -> None:
    if path.exists():
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()


def write_text_if_missing(path: Path, text: str) -> None:
    if not path.exists():
        path.write_text(text, encoding="utf-8")


def read_reference(name: str, fallback: str) -> str:
    reference = Path(__file__).resolve().parents[1] / "references" / name
    if reference.exists():
        return reference.read_text(encoding="utf-8")
    return fallback


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default="./workflow_cards")
    parser.add_argument("--zotero-collection", default="")
    parser.add_argument("--obsidian-vault", default="")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    cards = root / "cards"
    synthesis = root / "synthesis"
    cards.mkdir(parents=True, exist_ok=True)
    synthesis.mkdir(parents=True, exist_ok=True)

    config = root / "config.yaml"
    write_text_if_missing(
        config,
        "\n".join(
            [
                f'project_root: "{root}"',
                f'cards_folder: "{cards}"',
                f'matrix_path: "{root / "workflow_matrix.csv"}"',
                f'screening_path: "{root / "screening_decisions.csv"}"',
                f'search_protocol_path: "{root / "search_protocol.md"}"',
                f'synthesis_folder: "{synthesis}"',
                f'validation_script: "{Path(__file__).resolve().parent / "validate_project.py"}"',
                f'controlled_vocabularies: "{Path(__file__).resolve().parents[1] / "references" / "controlled_vocabularies.md"}"',
                f'zotero_collection: "{args.zotero_collection}"',
                f'obsidian_vault: "{args.obsidian_vault}"',
                "",
            ]
        ),
    )

    write_csv_if_missing(root / "workflow_matrix.csv", MATRIX_COLUMNS)
    write_csv_if_missing(root / "screening_decisions.csv", SCREENING_COLUMNS)
    write_text_if_missing(
        root / "search_protocol.md",
        read_reference(
            "search_protocol_template.md",
            "# Search Protocol\n\nPurpose: build a workflow-design literature map.\n",
        ),
    )
    write_text_if_missing(
        synthesis / "workflow_design_principles.md",
        "# Workflow Design Principles\n\n",
    )
    write_text_if_missing(
        synthesis / "batch_001_synthesis.md",
        read_reference(
            "batch_synthesis_template.md",
            "# Batch Synthesis: batch-001\n\n",
        ),
    )

    print(f"Project root: {root}")
    print(f"Cards folder: {cards}")
    print(f"Workflow Matrix: {root / 'workflow_matrix.csv'}")
    print(f"Screening decisions: {root / 'screening_decisions.csv'}")
    print(f"Batch synthesis template: {synthesis / 'batch_001_synthesis.md'}")
    print(f"Config: {config}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
