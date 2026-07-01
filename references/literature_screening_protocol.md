# Literature Screening Protocol

Use this protocol before generating Workflow Cards. The goal is not a clinical meta-analysis; it is a reproducible workflow-design literature map that identifies papers worth converting into Workflow Cards and then into the Workflow Matrix.

Reporting references:

- PRISMA 2020: https://www.prisma-statement.org/prisma-2020
- PRISMA-Search: https://www.prisma-statement.org/prisma-search

## Fixed objects

Use these names consistently:

- **Literature Screening Protocol**: this reproducible protocol for finding, deduplicating, and screening papers.
- **Evidence-Chain Analysis Prompt**: the question list used after a paper passes screening.
- **Workflow Card**: the complete Markdown note for one included paper.
- **Workflow Matrix**: the CSV table for cross-paper comparison.

## Review question

Define the screening question before searching:

```text
Which computational biology papers use a clear evidence-building workflow to prove a biological story, and what reusable workflow-design principles can be extracted from them?
```

Customize these fields in `search_protocol.md`:

| Field | Fill in |
|---|---|
| Domain | cancer, immunology, single-cell, spatial, multi-omics, public-data mining, or another scope |
| Biological object | cell type, disease, tissue, pathway, phenotype, treatment response, or atlas object |
| Data modality | scRNA-seq, snRNA-seq, spatial transcriptomics, bulk RNA-seq, proteomics, multi-omics, imaging, clinical data |
| Workflow focus | atlas, trajectory, reference mapping, spatial ecology, clinical translation, classifier/tool-building, perturbation |
| Required evidence | data credibility, cell identity, main claim evidence, validation layer |
| Exclusions | review, protocol, editorial, insufficient methods, unavailable full text, not workflow-relevant |

## Source plan

Use Zotero as the paper library and candidate source. Keep analysis outputs outside Zotero.

1. Run Zotero readiness:

   ```bash
   python <zotero-plugin-root>/skills/zotero/scripts/zotero.py status --json
   ```

2. If the local API is not running, open Zotero Desktop or run the Zotero skill's enable/restart command when the user wants Codex to operate Zotero.
3. Search Zotero with concrete query strings and export JSON:

   ```bash
   python <zotero-plugin-root>/skills/zotero/scripts/zotero.py search "single-cell cancer trajectory" --with-bibtex-keys --json > zotero_search.json
   ```

4. Import candidates into the screening table:

   ```bash
   python scripts/import_zotero_candidates.py --project-root ./workflow_cards --zotero-json zotero_search.json --query-id Q1 --search-query "single-cell cancer trajectory"
   ```

5. For each candidate, update `screening_decisions.csv`. Do not create a Workflow Card until enough article content exists.

## Screening levels

| Level | Input | Action | Output status |
|---|---|---|---|
| L0 Identification | Zotero search result, imported BibTeX/RIS, DOI, PMID, or seed list | Record candidate and search source | `candidate` |
| L1 Title/abstract screen | Metadata and abstract | Decide broad relevance | `included`, `excluded`, or `needs-full-text` |
| L2 Full-text eligibility | Full text, methods, figures, supplement, or indexed full text | Decide whether the workflow can be analyzed | `included`, `excluded`, `partial-card`, or `needs-full-text` |
| L3 Workflow Card readiness | Enough methods/results to answer the Evidence-Chain Analysis Prompt | Generate Workflow Card and update Workflow Matrix | `full-card` |

## Inclusion criteria

Include papers when all are true:

- The paper has a biological question or story, not only a software benchmark.
- The paper contains a computational workflow that builds evidence across data, annotation, discovery, and validation.
- The workflow is relevant to the selected domain and modality.
- The text provides enough methods/results to judge data credibility, cell identity or object definition, and support for the main claim.
- The paper can teach a reusable design principle.

## Exclusion criteria

Exclude or defer papers when any are true:

- Review, editorial, commentary, news, protocol-only, or perspective article.
- Abstract-only or metadata-only record with no accessible full text.
- Not in the selected biological or workflow domain.
- No analyzable computational workflow.
- Methods are too incomplete to connect claims to evidence.
- Duplicate of a record already screened.

## Decision rules

- If only metadata or abstract is available, set `screening_status=needs-full-text`; do not generate a Workflow Card.
- If full text is available but a key layer is missing, set `screening_status=partial-card` and mark missing fields as `unable to determine`.
- If excluded, fill `exclusion_reason` with one primary reason.
- If duplicated, set `screening_status=duplicate` and fill `duplicate_of`.
- If included and ready, generate a Workflow Card, then update the Workflow Matrix and set `screening_status=full-card`.
- Never invent missing methods, datasets, validation, or conclusions.

## Zotero to Workflow Card handoff

Use Zotero for:

- metadata search
- Zotero item keys
- BibTeX keys
- citation export
- indexed full text when explicitly needed
- attachment paths only when the user asks

Use this skill for:

- `search_protocol.md`
- `screening_decisions.csv`
- Workflow Cards
- `workflow_matrix.csv`

Do not write tags, notes, or collections back to Zotero unless the user explicitly asks for a Zotero write action.

## Required screening fields

`screening_decisions.csv` records one row per candidate paper. Required columns are:

| Column | Meaning |
|---|---|
| screening_id | Stable row ID, often `query_id:zotero_item_key` |
| search_round | Search or screening batch name |
| query_id | Short ID for one query in `search_protocol.md` |
| source_database | Zotero local library, PubMed, Web of Science, Google Scholar, citation chasing, manual seed, etc. |
| search_query | Query that found the candidate |
| retrieved_date | ISO date when the candidate was recorded |
| paper_id | Stable local ID |
| title | Paper title |
| year | Publication year |
| journal | Journal or source title |
| doi | DOI |
| pmid | PubMed ID |
| url | URL if available |
| authors | Creator summary |
| abstract_available | yes, no, unknown |
| full_text_available | yes, no, unknown |
| zotero_target_collection | Zotero collection used or intended |
| zotero_item_key | Zotero item key, not BibTeX key |
| bibtex_key | Exported citation key if available |
| zotero_status | in-library, imported, not-imported, missing, duplicate |
| topic_fit | yes, no, uncertain |
| workflow_relevance | high, medium, low, none, uncertain |
| data_relevance | high, medium, low, none, uncertain |
| public_data_relevance | high, medium, low, none, uncertain |
| method_signal | atlas, trajectory, spatial, communication, GRN, clinical, classifier, tool, mixed, unclear |
| study_scope | brief description of biological scope |
| cell_type | Main cell type or tissue object |
| cancer_type | Cancer or disease context |
| data_type | scRNA-seq, snRNA-seq, spatial, bulk, multi-omics, etc. |
| workflow_type_hint | Expected Workflow Card category |
| inclusion_decision | include, exclude, maybe, pending |
| exclusion_reason | Primary exclusion reason when excluded |
| duplicate_of | `paper_id`, DOI, or Zotero item key of the retained record |
| decision_reason | Short reason for the current decision |
| screening_status | candidate, included, excluded, needs-full-text, partial-card, full-card, duplicate |
| needs_full_text | yes, no, unknown |
| action_next | title-abstract-screen, fetch-full-text, make-workflow-card, update-matrix, exclude, deduplicate |
| priority | high, medium, low |
| reviewer | Person or agent making the decision |
| workflow_card_status | not-started, partial-card, full-card, matrix-updated |
| card_path | Workflow Card path when generated |
| notes | Free-text uncertainty or next action |

## Minimal project loop

```text
Zotero search or imported source
-> import candidates into screening_decisions.csv
-> title/abstract screen
-> full-text eligibility screen
-> generate Workflow Card only for eligible papers
-> update workflow_matrix.csv
-> synthesize workflow design principles
```
