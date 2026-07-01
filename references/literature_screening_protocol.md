# Literature Screening Protocol

Use this protocol before generating Workflow Cards. The goal is not to collect many related papers or to run a clinical meta-analysis. The goal is to build a reproducible workflow-design literature map: a corpus of papers that teaches how biological questions, data choices, and computational workflows fit together.

Reporting references:

- PRISMA 2020: https://www.prisma-statement.org/prisma-2020
- PRISMA-Search: https://www.prisma-statement.org/prisma-search

## Contents

- Fixed objects
- Review question
- Search design
- Search round vs screening batch
- Zotero handoff
- Screening levels
- Decision rules
- Inclusion and exclusion criteria
- Required screening fields
- Batch synthesis

## Fixed Objects

Use these names consistently:

- **Literature Screening Protocol**: the reproducible search, deduplication, screening, and prioritization protocol used before full paper analysis.
- **Evidence-Chain Analysis Prompt**: the question list used after a paper passes screening.
- **Workflow Card**: the complete Markdown note for one eligible paper.
- **Workflow Matrix**: the CSV table for cross-paper comparison.

## Review Question

Default screening question:

```text
Which single-cell, pan-cancer, tumor immunology, spatial, multi-omics, or public-data papers are useful for learning how different biological questions require different workflow designs?
```

Customize this question in `search_protocol.md` before searching:

| Field | Fill in |
|---|---|
| Domain | cancer, immunology, single-cell, spatial, multi-omics, public-data mining, or another scope |
| Biological object | cell type, disease, tissue, pathway, phenotype, treatment response, or atlas object |
| Data modality | scRNA-seq, snRNA-seq, spatial transcriptomics, bulk RNA-seq, proteomics, multi-omics, imaging, clinical data |
| Workflow focus | atlas, trajectory, reference mapping, spatial ecology, clinical translation, classifier/tool-building, perturbation |
| Required evidence | data credibility, cell identity or object definition, main claim evidence, validation layer |
| Exclusions | review, protocol, editorial, unavailable full text, insufficient methods, not workflow-relevant |

## Search Design

Build search terms from three axes:

| Axis | Purpose | Example terms |
|---|---|---|
| Domain axis | Keeps the corpus in the right scientific area | single-cell, pan-cancer, tumor microenvironment, immunotherapy, spatial transcriptomics |
| Workflow axis | Captures workflow diversity | atlas, reference mapping, trajectory, cell-cell communication, spatial niche, classifier, public data |
| Object axis | Optional balancing or subproject terms | NK cells, dendritic cells, myeloid, T cells, tumor-infiltrating lymphocytes |

Good broad pattern:

```text
("single-cell" OR scRNA-seq OR snRNA-seq OR spatial transcriptomics)
AND (cancer OR tumor OR immunotherapy OR "tumor microenvironment")
AND (atlas OR workflow OR trajectory OR "cell-cell communication" OR "reference mapping" OR classifier)
```

Do not over-narrow the first search by a single cell type such as NK, DC, T cell, or macrophage unless the user explicitly wants a cell-type-specific subproject. Use cell-type terms later for balancing, gap filling, or focused comparison.

Record each query in `search_protocol.md` with:

- `query_id`
- date
- database or source
- exact query
- filters
- result count
- reason for the query

## Search Round vs Screening Batch

A search round is the retrieval event. It may return hundreds or thousands of records.

A screening batch is the subset reviewed in one pass. Use 20-50 papers per batch by default.

After each batch, update:

- workflow types covered
- data types covered
- cancer or immune contexts covered
- excluded-paper patterns
- missing workflow categories
- next query adjustment

## Zotero Handoff

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

Do not write Zotero tags, notes, or collections by default. Zotero writes require explicit user intent.

## Screening Levels

| Level | Input | Action | Output status |
|---|---|---|---|
| L0 Identification | Zotero search result, imported BibTeX/RIS, DOI, PMID, citation chase, or seed list | Record candidate and search source | `candidate` |
| L1 Title/abstract screen | Metadata and abstract | Decide broad relevance | `title-abstract-screened`, `included-for-full-text`, `excluded`, or `needs-full-text` |
| L2 Full-text eligibility | Full text, methods, figures, supplement, or indexed full text | Decide whether the workflow can be analyzed | `ready-for-workflow-card`, `excluded`, `partial-card`, `needs-full-text`, or `hold` |
| L3 Workflow Card readiness | Enough methods/results to answer the Evidence-Chain Analysis Prompt | Generate Workflow Card and update Workflow Matrix | `full-card` |

Canonical `screening_status` values:

```text
candidate, title-abstract-screened, included-for-full-text, excluded,
needs-full-text, ready-for-workflow-card, partial-card, full-card,
duplicate, hold
```

## Decision Rules

- If only metadata or abstract is available, update `screening_decisions.csv`; do not generate a Workflow Card.
- If title/abstract screening passes but full text is still needed, set `screening_status=included-for-full-text` or `screening_status=needs-full-text`.
- If full text is available and enough methods/results exist, set `screening_status=ready-for-workflow-card`.
- If full text is available but a key layer is missing, set `screening_status=partial-card` and mark missing fields as `unable to determine`.
- If excluded, fill `exclusion_reason` with one primary reason.
- If duplicated, set `screening_status=duplicate` and fill `duplicate_of`.
- If a Workflow Card is generated, update the Workflow Matrix and set `screening_status=full-card`.
- Never invent missing methods, datasets, validation, or conclusions.

## Inclusion Criteria

Include or prioritize papers when at least one is true:

- strong example of a workflow type
- unusual or valuable workflow architecture, such as branching, parallel analysis, or convergence across modalities
- clear public-data selection strategy
- strong link between biological question, data design, and computational workflow
- useful contrast against already-screened papers
- high-value review, benchmark, or methods paper that helps interpret workflows

## Exclusion Criteria

Exclude or deprioritize papers when:

- the article type is review, editorial, commentary, news, protocol-only, or perspective and it does not help workflow interpretation
- the topic is relevant but the workflow is routine and not reusable
- only a result is visible and the evidence chain cannot be reconstructed
- data source or metadata are too unclear for the intended analysis
- the paper is a duplicate
- the paper would bias the corpus toward one cell type, cancer type, method, or lab without adding workflow diversity

## Required Screening Fields

`screening_decisions.csv` records one row per candidate paper.

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
| abstract_available | yes, no, unable to determine |
| full_text_available | yes, no, unable to determine |
| zotero_target_collection | Zotero collection used or intended |
| zotero_item_key | Zotero item key, not BibTeX key |
| bibtex_key | Exported citation key if available |
| zotero_status | in-library, not-in-zotero, import-needed, imported, skipped, missing, duplicate, unable-to-check |
| topic_fit | yes, no, uncertain, pending, or unable to determine |
| workflow_relevance | high, medium, low, none, uncertain, pending, or unable to determine |
| data_relevance | high, medium, low, none, uncertain, pending, or unable to determine |
| public_data_relevance | high, medium, low, none, uncertain, pending, or unable to determine |
| method_signal | atlas, mapping, trajectory, spatial, communication, classifier, clinical, public-data, multi-omics, etc. |
| study_scope | single cancer, pan-cancer, cross-cohort, atlas, method/tool, review, benchmark, etc. |
| cell_type | Main cell type, tissue object, or immune compartment |
| cancer_type | Cancer or disease context |
| data_type | scRNA-seq, snRNA-seq, spatial, bulk, multi-omics, public data, etc. |
| workflow_type_hint | Initial guess before full Workflow Card |
| inclusion_decision | include, exclude, maybe, pending, uncertain, or defer |
| exclusion_reason | Primary exclusion reason when excluded |
| duplicate_of | `paper_id`, DOI, or Zotero item key of the retained record |
| decision_reason | One-sentence reason for the current decision |
| screening_status | candidate, title-abstract-screened, included-for-full-text, excluded, needs-full-text, ready-for-workflow-card, partial-card, full-card, duplicate, hold |
| priority | high, medium, low |
| design_sample_role | pending, canonical-example, contrast-case, counterexample, gap-filler, method-reference, validation-reference |
| needs_full_text | yes, no, or unable to determine |
| action_next | title-abstract-screen, import-to-zotero, fetch-full-text, retrieve-full-text, review-methods, make-workflow-card, update-matrix, update-card, exclude, deduplicate, hold |
| reviewer | Person or agent making the decision |
| workflow_card_status | not-started, partial-card, full-card, matrix-updated, not-needed |
| card_path | Workflow Card path when generated |
| notes | Free-text uncertainty or next action |

Use `unable to determine` instead of inventing metadata or methods.

Use `references/controlled_vocabularies.md` when choosing repeatable values for screening status, method signals, workflow hints, data types, and design sample roles.

## Batch Synthesis

After each screening batch, do not only count included papers. Extract what comparison is teaching:

- Which workflow types are overrepresented or missing?
- Which biological questions consistently require which data designs?
- Which workflows depend most on annotation quality?
- Which workflows depend most on public-data selection and metadata completeness?
- Which tools appear as technical choices because of the biological question, rather than because they are fashionable?
- Which papers are positive controls, negative controls, or counterexamples for workflow design?

The endpoint is a growing map of research-design principles, not a bigger bibliography.
