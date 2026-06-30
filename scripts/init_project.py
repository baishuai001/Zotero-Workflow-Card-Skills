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
    "card_path",
]


SCREENING_COLUMNS = [
    "paper_id",
    "title",
    "doi",
    "zotero_item_key",
    "screening_status",
    "decision_reason",
    "needs_full_text",
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
        "# Search Protocol\n\nPurpose: build a workflow-design literature map.\n",
    )
    write_text_if_missing(
        synthesis / "workflow_design_principles.md",
        "# Workflow Design Principles\n\n",
    )

    print(f"Project root: {root}")
    print(f"Cards folder: {cards}")
    print(f"Workflow Matrix: {root / 'workflow_matrix.csv'}")
    print(f"Screening decisions: {root / 'screening_decisions.csv'}")
    print(f"Config: {config}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
