---
name: zotero-workflow-card
description: Use when analyzing papers from Zotero or literature searches into Workflow Cards, saving one Markdown card per paper, updating a workflow_matrix.csv for cross-paper comparison, or building a workflow-design literature map.
---

# Zotero Workflow Card

## Core Rule

Use exactly these three names:

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
| `screening_decisions.csv` | Inclusion/exclusion and screening status |

Do not write the full Workflow Card into Zotero by default. Zotero notes/tags are optional future enhancements, not v0.1 behavior.

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
    `-- workflow_design_principles.md
```

Always report the absolute paths written. Tell the user that paths can be changed by editing `config.yaml` or by passing script arguments.

## Workflow

1. Identify the source paper from Zotero, a DOI/PMID/URL, or supplied paper text/PDF.
2. Confirm whether enough content exists for a full Workflow Card:
   - Metadata or abstract only: make a screening record, not a full Workflow Card.
   - Full text, methods, or sufficient article content: make a full Workflow Card.
3. Use `references/evidence_chain_analysis_prompt.md` as the analysis protocol.
4. Save the complete single-paper result as a Workflow Card using `references/workflow_card_template.md`.
5. Update the Workflow Matrix using `references/workflow_matrix_schema.md`.
6. Report written paths and any fields marked "unable to determine".

## Zotero Use

When using Zotero, first use the installed Zotero skill or its helper to check readiness. Prefer read-only operations for search, metadata retrieval, BibTeX export, and indexed full text. Treat importing records or modifying a Zotero library as an explicit write action requiring user intent.

v0.1 does not require Zotero tag or note writes.

Never write Zotero tags, notes, or collections as part of the default Workflow Card flow. If a user explicitly asks to manage Zotero records, use the Zotero skill directly and treat that as a separate Zotero write action.

## Scripts

Use these scripts for deterministic file operations:

```bash
python scripts/init_project.py --project-root ./workflow_cards
python scripts/write_workflow_card.py --project-root ./workflow_cards --slug paper-slug --content-file card.md
python scripts/update_workflow_matrix.py --project-root ./workflow_cards --row-json row.json
python scripts/update_screening_decisions.py --project-root ./workflow_cards --row-json screening-row.json
```

Script roles:

- `init_project.py`: create the default project folders and empty tracking files.
- `write_workflow_card.py`: save one complete Workflow Card Markdown file.
- `update_workflow_matrix.py`: upsert one paper row in `workflow_matrix.csv`.
- `update_screening_decisions.py`: upsert a candidate, included, excluded, partial-card, or needs-full-text decision in `screening_decisions.csv`.

## Quality Rules

- Never invent missing methods, datasets, tools, or conclusions.
- If only abstract/metadata are available, mark fields as `unable to determine`.
- Separate evidence from inference.
- In every final response, name the Workflow Card path and Workflow Matrix path if either was written.
- Preserve the distinction between Zotero item keys and BibTeX keys when reporting citation data.
