# Screening Decisions Schema

`screening_decisions.csv` tracks candidate papers before and during Workflow Card generation.

One row equals one candidate paper from a search result, Zotero collection, citation chase, or manual seed list.

Required columns:

| Column | Meaning |
|---|---|
| screening_id | Stable local screening ID |
| search_round | Search round or batch label, such as `round-001` |
| query_id | Query identifier from `search_protocol.md` |
| source_database | PubMed, Web of Science, Google Scholar, Zotero, citation-chase, manual, etc. |
| search_query | Exact or shortened query that retrieved the paper |
| retrieved_date | Date the record was retrieved |
| paper_id | Stable local paper ID |
| title | Paper title |
| year | Publication year |
| journal | Journal or source |
| doi | DOI |
| pmid | PubMed ID if available |
| url | URL if DOI/PMID is unavailable |
| authors | Short author string |
| abstract_available | yes, no, or unable to determine |
| full_text_available | yes, no, or unable to determine |
| zotero_target_collection | Intended Zotero collection name |
| zotero_item_key | Zotero item key, not BibTeX key |
| bibtex_key | Exported citation key if available |
| zotero_status | in-library, not-in-zotero, import-needed, imported, missing, duplicate, unable-to-check |
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
| exclusion_reason | Controlled short reason when excluded |
| duplicate_of | `paper_id`, DOI, or Zotero item key of the retained record |
| decision_reason | One-sentence reason for the current decision |
| screening_status | candidate, title-abstract-screened, included-for-full-text, excluded, needs-full-text, ready-for-workflow-card, partial-card, full-card, duplicate, hold |
| priority | high, medium, low |
| design_sample_role | pending, canonical-example, contrast-case, counterexample, gap-filler, method-reference, validation-reference |
| needs_full_text | yes, no, or unable to determine |
| action_next | title-abstract-screen, import-to-zotero, fetch-full-text, retrieve-full-text, review-methods, make-workflow-card, update-matrix, update-card, exclude, deduplicate, hold |
| reviewer | Person or agent making the decision |
| workflow_card_status | not-started, partial-card, full-card, matrix-updated, not-needed |
| card_path | Absolute or project-relative path to Workflow Card |
| notes | Free text |

Use `unable to determine` instead of inventing metadata or methods.
