---
name: zotero-workflow-card
description: Use when screening literature from Zotero or searches for a workflow-design corpus, analyzing papers into Workflow Cards, saving one Markdown card per paper, updating workflow_matrix.csv, or building a cross-paper workflow-design map.
---

# Zotero Workflow Card

## Core Rule

Use exactly these four names:

- **Literature Screening Protocol**: the reproducible search, deduplication, screening, and prioritization protocol used before full paper analysis.
- **Evidence-Chain Analysis Prompt**: the question list used to analyze how one paper organizes evidence to prove a biological story.
- **Workflow Card**: the complete Markdown note for one paper, generated from the Evidence-Chain Analysis Prompt.
- **Workflow Matrix**: the CSV table where each row is one paper and selected fields from its Workflow Card are compressed for cross-paper comparison.

Do not rename these concepts in user-facing explanations.

## Storage Roles

Keep storage responsibilities separate:

| Place | Store |
|---|---|
| Zotero | Paper metadata, PDFs, attachments, citation data |
| Markdown or Obsidian folder | One complete Workflow Card per paper |
| `workflow_matrix.csv` | One row per paper for cross-paper comparison |
| `search_protocol.md` | Project copy of the Literature Screening Protocol, search queries, batches, result counts, and coverage gaps |
| `screening_decisions.csv` | Candidate records, inclusion/exclusion decisions, Zotero linkage, and Workflow Card handoff status |
| `synthesis/batch_*.md` | Batch-level lessons, coverage gaps, and next-query decisions |

Do not write the full Workflow Card into Zotero by default. Zotero notes/tags are optional future enhancements, not default behavior.

## Default Project

If the user does not provide an output path, create and use:

```text
./workflow_cards
```

Default structure:

```text
workflow_cards/
|-- config.yaml
|-- workflow_matrix.csv
|-- screening_decisions.csv
|-- search_protocol.md
|-- cards/
`-- synthesis/
    |-- batch_001_synthesis.md
    `-- workflow_design_principles.md
```

Always report the absolute paths written. Tell the user that paths can be changed by editing `config.yaml` or by passing script arguments.

## Workflow

1. If the user is screening many papers, use `references/literature_screening_protocol.md` first and record candidates in `screening_decisions.csv`.
2. Identify the source paper from Zotero, a DOI/PMID/URL, or supplied paper text/PDF.
3. Confirm whether enough content exists for a full Workflow Card:
   - Metadata or abstract only: make or update a screening record, not a full Workflow Card.
   - Full text, methods, or sufficient article content: make a full Workflow Card.
4. Use `references/evidence_chain_analysis_prompt.md` as the analysis protocol.
5. Save the complete single-paper result as a Workflow Card using `references/workflow_card_template.md`.
6. Prefer `finalize_workflow_card.py` to write the Workflow Card, update the Workflow Matrix, backfill `screening_decisions.csv`, and run validation in one closure step.
7. Report written paths and any fields marked "unable to determine".

## Literature Screening

Use `references/literature_screening_protocol.md` when the task is to find, screen, prioritize, or compare many papers before full reading.

Screening flow:

```text
search result -> screening_decisions.csv -> Zotero item/full text -> Workflow Card -> Workflow Matrix
```

Use `references/screening_decisions_schema.md` for screening fields and allowed meanings; use `references/literature_screening_protocol.md` for the screening process.
Use `references/controlled_vocabularies.md` when choosing repeatable values such as `screening_status`, `method_signal`, `workflow_type_hint`, `data_type`, and `design_sample_role`.

Default decision rule:

- If only title/abstract/metadata are available, update `screening_decisions.csv`.
- If selected but not in Zotero, mark `zotero_status` as `import-needed`; do not import unless the user explicitly asks.
- If title/abstract screening passes but full text is still needed, set `inclusion_decision=include`, `screening_status=included-for-full-text`, and `action_next=retrieve-full-text`.
- If full text/methods are sufficient and the paper is useful for workflow design, set `inclusion_decision=include`, `screening_status=ready-for-workflow-card`, and `action_next=make-workflow-card`.
- If a Workflow Card is generated, update both `workflow_matrix.csv` and the matching screening row.

The purpose of screening is to build a representative corpus of workflow-design examples. Avoid over-narrowing the first search by a single cell type unless the user asks for that subproject.

Canonical `screening_status` values:

```text
candidate, title-abstract-screened, included-for-full-text, excluded,
needs-full-text, ready-for-workflow-card, partial-card, full-card,
duplicate, hold
```

Use `design_sample_role` to record why a paper belongs in the corpus:

```text
pending, canonical-example, contrast-case, counterexample,
gap-filler, method-reference, validation-reference
```

After each 20-50 paper screening batch, update or create a batch synthesis note from `references/batch_synthesis_template.md`.

Use a combined stop / continue decision after each batch:

- **practical threshold**: the pilot or phase has reached its planned count, such as 10-20 screened candidates, 3-5 Workflow Cards for a pilot, or about 50 screened candidates and 10-15 Workflow Cards for a first phase.
- **design saturation**: new papers no longer add new workflow types, data-selection patterns, validation strategies, or reusable design principles.

Treat design saturation as a checklist, not a feeling:

- main workflow types have representative papers
- each important workflow type has at least one canonical-example and contrast-case
- public-data strategies have enough cases to compare selection, metadata, reuse, and validation logic
- key data modalities are not badly imbalanced
- newly screened papers no longer create new workflow design principles
- the corpus can guide the user's own public-data screening and study design

Continue searching when either practical threshold is not met or design saturation is not yet credible. Stop or move to final synthesis only when both are met for the current project phase.

## User-Supplied Papers

Treat papers supplied by the user as manual seed records. The user can provide a DOI, PMID, URL, Zotero item key, PDF path, or pasted full text. An official journal URL is helpful but not required when DOI, PMID, Zotero metadata, or enough citation information exists.

For one user-supplied paper, route it through the same readiness gate:

- Metadata, abstract, or citation only: add or update a `screening_decisions.csv` row with `source_database=manual-seed`, `search_round=manual-seed-001`, `query_id=USER-SEED-001`, and the appropriate next action.
- Full text, methods, indexed Zotero full text, local PDF, or pasted article text: generate a Workflow Card and close it with `finalize_workflow_card.py`.

For many user-supplied papers, accept a Zotero collection name, Zotero item keys, DOI/PMID list, URLs, local PDF paths, BibTeX/RIS, CSV/TSV, Markdown list, or pasted text, then import them as manual-seed candidates before screening.

## Single-Paper Workflow

1. Identify the source paper from Zotero, a DOI/PMID/URL, or supplied paper text/PDF.
2. Confirm whether enough content exists for a full Workflow Card:
   - Metadata or abstract only: make a screening record, not a full Workflow Card.
   - Full text, methods, or sufficient article content: make a full Workflow Card.
3. Use `references/evidence_chain_analysis_prompt.md` as the analysis protocol.
4. Save the complete single-paper result as a Workflow Card using `references/workflow_card_template.md`.
5. Use `finalize_workflow_card.py` to update the Workflow Matrix and backfill `screening_decisions.csv`.
6. Report written paths and any fields marked "unable to determine".

## Zotero Use

When using Zotero, first use the installed Zotero skill or its helper to check readiness. Prefer read-only operations for search, metadata retrieval, BibTeX export, and indexed full text. Treat importing records or modifying a Zotero library as an explicit write action requiring user intent.

The default flow does not require Zotero tag or note writes.

Never write Zotero tags, notes, or collections as part of the default Workflow Card flow. If a user explicitly asks to manage Zotero records, use the Zotero skill directly and treat that as a separate Zotero write action.

## Scripts

Use these scripts for deterministic file operations:

```bash
python scripts/init_project.py --project-root ./workflow_cards
python scripts/import_zotero_candidates.py --project-root ./workflow_cards --zotero-json zotero_search.json --query-id Q1 --search-query "single-cell cancer trajectory"
python scripts/write_workflow_card.py --project-root ./workflow_cards --slug paper-slug --content-file card.md
python scripts/update_workflow_matrix.py --project-root ./workflow_cards --row-json row.json
python scripts/update_screening_decisions.py --project-root ./workflow_cards --row-json screening-row.json
python scripts/finalize_workflow_card.py --project-root ./workflow_cards --slug paper-slug --content-file card.md --row-json row.json
python scripts/validate_project.py --project-root ./workflow_cards
```

Script roles:

- `init_project.py`: create the default project folders and empty tracking files.
- `import_zotero_candidates.py`: import Zotero search JSON into `screening_decisions.csv` as candidate rows.
- `write_workflow_card.py`: save one complete Workflow Card Markdown file.
- `update_workflow_matrix.py`: upsert one paper row in `workflow_matrix.csv`.
- `update_screening_decisions.py`: upsert screening decisions while preserving existing non-empty row fields.
- `finalize_workflow_card.py`: close the Workflow Card handoff by writing the card, updating the Workflow Matrix, backfilling `screening_decisions.csv`, and running validation.
- `validate_project.py`: validate status values, duplicate identifiers, card paths, and screening-to-matrix handoff consistency.

## Quality Rules

- Never invent missing methods, datasets, tools, or conclusions.
- If only abstract/metadata are available, mark fields as `unable to determine`.
- Separate evidence from inference.
- Run `validate_project.py` after batch screening or bulk Workflow Card updates.
- In every final response, name the Workflow Card path and Workflow Matrix path if either was written.
- Preserve the distinction between Zotero item keys and BibTeX keys when reporting citation data.
