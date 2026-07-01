#!/usr/bin/env python3
"""Import Zotero search JSON as candidate rows in screening_decisions.csv."""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import date
from pathlib import Path
from typing import Any


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
    "needs_full_text",
    "action_next",
    "reviewer",
    "workflow_card_status",
    "card_path",
    "notes",
]


def as_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("items", "results", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    raise SystemExit("Zotero JSON must be a list of items or an object with items/results/data")


def normalized_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(str(item) for item in value if item is not None)
    return str(value)


def parse_pmid(*values: Any) -> str:
    for value in values:
        text = normalized_text(value)
        match = re.search(r"\bPMID\s*[:#]?\s*(\d+)\b", text, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return ""


def first_value(*values: Any) -> str:
    for value in values:
        text = normalized_text(value).strip()
        if text:
            return text
    return ""


def row_key(row: dict[str, str]) -> tuple[str, str]:
    for key in ("doi", "pmid", "zotero_item_key", "paper_id", "screening_id", "title"):
        value = (row.get(key) or "").strip().lower()
        if value:
            return key, value
    raise SystemExit("Row needs at least one of doi, zotero_item_key, paper_id, or title")


def load_existing(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [{column: row.get(column, "") for column in COLUMNS} for row in reader]


def upsert(rows: list[dict[str, str]], new_row: dict[str, str]) -> tuple[list[dict[str, str]], bool]:
    match_key, match_value = row_key(new_row)
    output: list[dict[str, str]] = []
    updated = False
    for row in rows:
        if (row.get(match_key) or "").strip().lower() == match_value:
            merged = dict(row)
            for column, value in new_row.items():
                if value:
                    merged[column] = value
            output.append(merged)
            updated = True
        else:
            output.append(row)
    if not updated:
        output.append(new_row)
    return output, updated


def item_to_row(item: dict[str, Any], args: argparse.Namespace) -> dict[str, str]:
    data = item.get("data") if isinstance(item.get("data"), dict) else item
    key = first_value(item.get("key"), data.get("key"), item.get("zotero_item_key"))
    title = first_value(data.get("title"), item.get("title"))
    doi = first_value(data.get("DOI"), data.get("doi"), item.get("doi"))
    pmid = first_value(data.get("PMID"), data.get("pmid"), parse_pmid(data.get("extra"), item.get("extra")))
    paper_id = first_value(args.paper_id_prefix + key if key and args.paper_id_prefix else "", key, doi, title)
    screening_id = first_value(
        f"{args.query_id}:{key}" if args.query_id and key else "",
        f"{args.query_id}:{doi}" if args.query_id and doi else "",
        paper_id,
    )
    return {
        "screening_id": screening_id,
        "search_round": args.search_round,
        "query_id": args.query_id,
        "source_database": args.source_database,
        "search_query": args.search_query,
        "retrieved_date": args.retrieved_date,
        "paper_id": paper_id,
        "title": title,
        "year": first_value(data.get("year"), item.get("year"), data.get("date")),
        "journal": first_value(data.get("publicationTitle"), data.get("journalAbbreviation"), item.get("journal")),
        "doi": doi,
        "pmid": pmid,
        "url": first_value(data.get("url"), item.get("url")),
        "authors": first_value(item.get("creators"), data.get("creators")),
        "abstract_available": "unknown",
        "full_text_available": "unknown",
        "zotero_target_collection": args.zotero_target_collection,
        "zotero_item_key": key,
        "bibtex_key": first_value(item.get("bibtexKey"), data.get("citationKey"), item.get("bibtex_key")),
        "zotero_status": "in-library",
        "topic_fit": "pending",
        "workflow_relevance": "pending",
        "data_relevance": "pending",
        "public_data_relevance": "pending",
        "method_signal": "pending",
        "study_scope": "",
        "cell_type": "",
        "cancer_type": "",
        "data_type": "",
        "workflow_type_hint": "",
        "inclusion_decision": "pending",
        "exclusion_reason": "",
        "duplicate_of": "",
        "decision_reason": "Imported from Zotero search",
        "screening_status": args.screening_status,
        "needs_full_text": "unknown",
        "action_next": "title-abstract-screen",
        "priority": args.priority,
        "reviewer": args.reviewer,
        "workflow_card_status": "not-started",
        "card_path": "",
        "notes": "",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default="./workflow_cards")
    parser.add_argument("--zotero-json", required=True, help="JSON from zotero.py search --json")
    parser.add_argument("--search-query", default="")
    parser.add_argument("--source-database", default="zotero-local")
    parser.add_argument("--retrieved-date", default=date.today().isoformat())
    parser.add_argument("--search-round", default="")
    parser.add_argument("--query-id", default="")
    parser.add_argument("--zotero-target-collection", default="")
    parser.add_argument("--screening-status", default="candidate")
    parser.add_argument("--priority", default="medium")
    parser.add_argument("--reviewer", default="")
    parser.add_argument("--paper-id-prefix", default="ZOTERO-")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    screening = root / "screening_decisions.csv"
    root.mkdir(parents=True, exist_ok=True)

    payload = json.loads(Path(args.zotero_json).read_text(encoding="utf-8-sig"))
    rows = load_existing(screening)
    added = 0
    updated = 0
    for item in as_items(payload):
        new_row = item_to_row(item, args)
        rows, was_updated = upsert(rows, new_row)
        if was_updated:
            updated += 1
        else:
            added += 1

    with screening.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Added {added}, updated {updated} candidate rows in {screening.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
