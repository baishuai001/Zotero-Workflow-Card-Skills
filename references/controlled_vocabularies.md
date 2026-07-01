# Controlled Vocabularies

Use these values to keep `screening_decisions.csv` and `workflow_matrix.csv` comparable across papers.

Prefer one value from the list. Use semicolons only when a paper genuinely has multiple roles or methods.

## screening_status

- `candidate`
- `title-abstract-screened`
- `included-for-full-text`
- `excluded`
- `needs-full-text`
- `ready-for-workflow-card`
- `partial-card`
- `full-card`
- `duplicate`
- `hold`

## workflow_card_status

- `not-started`
- `partial-card`
- `full-card`
- `matrix-updated`
- `not-needed`

## inclusion_decision

- `include`
- `exclude`
- `maybe`
- `pending`
- `uncertain`
- `defer`

## design_sample_role

- `pending`
- `canonical-example`: a strong positive example of a workflow type.
- `contrast-case`: useful mainly because it differs from another paper.
- `counterexample`: shows a weak, biased, incomplete, or misleading workflow design.
- `gap-filler`: covers an underrepresented workflow, modality, cancer type, or cell type.
- `method-reference`: helps interpret a method or benchmark rather than serving as the main biological example.
- `validation-reference`: useful because it demonstrates validation, clinical linkage, perturbation, or external confirmation.

## method_signal

- `atlas`
- `mapping`
- `trajectory`
- `spatial`
- `communication`
- `GRN`
- `clinical`
- `classifier`
- `tool`
- `public-data`
- `multi-omics`
- `mixed`
- `unclear`

## main_workflow_type / workflow_type_hint

- `reference mapping`
- `de novo atlas`
- `trajectory`
- `spatial ecology`
- `clinical translation`
- `classifier/tool-building`
- `public-data integration`
- `multi-omics integration`
- `perturbation`
- `benchmark`
- `review/method-reference`
- `unable to determine`

## data_type

- `scRNA-seq`
- `snRNA-seq`
- `spatial transcriptomics`
- `bulk RNA-seq`
- `single-cell multi-omics`
- `proteomics`
- `imaging`
- `clinical data`
- `public data`
- `multi-omics`
- `other`
- `unable to determine`

## zotero_status

- `in-library`
- `not-in-zotero`
- `import-needed`
- `imported`
- `skipped`
- `missing`
- `duplicate`
- `unable-to-check`

## action_next

- `title-abstract-screen`
- `import-to-zotero`
- `fetch-full-text`
- `retrieve-full-text`
- `review-methods`
- `make-workflow-card`
- `update-matrix`
- `update-card`
- `exclude`
- `deduplicate`
- `hold`

## priority

- `high`
- `medium`
- `low`
