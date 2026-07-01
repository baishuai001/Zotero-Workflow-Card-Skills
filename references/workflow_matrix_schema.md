# Workflow Matrix schema

`workflow_matrix.csv` is the cross-paper comparison table.

One row equals one paper. Columns are compressed fields extracted from the paper's Workflow Card.

Required columns:

| Column | Meaning |
|---|---|
| paper_id | Stable local ID |
| title | Paper title |
| year | Publication year |
| journal | Journal or source |
| doi | DOI |
| pmid | PubMed ID if available |
| zotero_item_key | Zotero item key, not BibTeX key |
| bibtex_key | Exported citation key if available |
| cell_type | Main cell type or tissue object |
| cancer_type | Cancer or disease context |
| data_type | scRNA-seq, snRNA-seq, spatial, bulk, multi-omics, etc. |
| core_question | One-sentence core scientific question |
| main_claims | Compressed main claims |
| data_credibility_basis | How data credibility was established |
| cell_identity_basis | How cell identity was established |
| conclusion_evidence_basis | What supports the main conclusion |
| data_supports_workflow | strong, medium, weak, or unable to determine |
| main_workflow_type | Main workflow category |
| workflow_trunk | Short trunk flow |
| downstream_modules | Semicolon-separated downstream modules |
| evidence_chain | Compressed claim-to-evidence mapping |
| key_technical_choices | Compressed key decisions |
| workflow_rationale | Why this workflow fits the paper |
| counterfactual_risk | What would be lost with another workflow |
| public_data_strategy | How public data were selected or used |
| reusable_design_principle | Main transferable research design lesson |
| limitations | Main limitations or uncertainties |
| screening_status | candidate, title-abstract-screened, included-for-full-text, excluded, needs-full-text, ready-for-workflow-card, partial-card, full-card, duplicate, hold |
| priority | high, medium, low |
| design_sample_role | How this paper functions in the workflow-design corpus: canonical-example, contrast-case, counterexample, gap-filler, method-reference, or validation-reference |
| card_path | Absolute or project-relative path to Workflow Card |

Screening details live in `screening_decisions.csv`; see `references/screening_decisions_schema.md`.
