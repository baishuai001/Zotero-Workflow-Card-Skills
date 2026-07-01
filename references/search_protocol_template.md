# Search Protocol

Purpose: build a workflow-design literature map.

## Review Question

```text
Which single-cell, pan-cancer, tumor immunology, spatial, multi-omics, or public-data papers are useful for learning how different biological questions require different workflow designs?
```

## Scope

| Field | Project value |
|---|---|
| Domain |  |
| Biological object |  |
| Data modality |  |
| Workflow focus |  |
| Required evidence |  |
| Exclusions |  |

## Query Log

| query_id | date | source_database | query | filters | result_count | reason |
|---|---|---|---|---|---:|---|
|  |  |  |  |  |  |  |

## Search Rounds

| search_round | date | source_database | query_ids | total_records | deduplicated_records | notes |
|---|---|---|---|---:|---:|---|
| round-001 |  |  |  |  |  |  |

## Screening Batches

| batch_id | search_round | date | reviewed_count | included | excluded | uncertain | workflow_gaps | next_query_change |
|---|---|---|---:|---:|---:|---:|---|---|
| batch-001 | round-001 |  |  |  |  |  |  |  |

## Coverage Notes

| Dimension | Covered | Missing or underrepresented | Next action |
|---|---|---|---|
| Workflow type |  |  |  |
| Data modality |  |  |  |
| Cancer or immune context |  |  |  |
| Public-data strategy |  |  |  |
| Validation strategy |  |  |  |

## Stop / Continue Criteria

Use this stop / continue rule after each screening batch: judge the practical count and design saturation together. The practical threshold is the count requirement inside each gate.

| Gate | Practical threshold | Saturation requirement | Current judgment | Action |
|---|---|---|---|---|
| Pilot gate | 10-20 screened candidates and 3-5 Workflow Cards | Draft the coverage map; identify obvious missing workflow types, modalities, and public-data patterns. |  | continue broad search / targeted gap filling |
| First-phase gate | about 50 screened candidates and 10-15 Workflow Cards | Major workflow types have representative papers; priority types have canonical-example and contrast-case candidates; obvious imbalance is known. |  | targeted gap filling / prepare synthesis |
| Formal-report gate | about 20 high-quality Workflow Cards | The corpus must satisfy the saturation checklist. |  | generate the formal report / continue targeted gap filling |

Design saturation checklist:

| Check | Current judgment | stop / continue action |
|---|---|---|
| main workflow types have representative papers |  |  |
| each important workflow type has at least one canonical-example and contrast-case |  |  |
| public-data strategies have enough cases |  |  |
| key data modalities are not badly imbalanced |  |  |
| newly screened papers no longer create new workflow design principles |  |  |
| the corpus can guide the user's own public-data screening and study design |  |  |

## Decisions

- Search adjustments:
- Known biases:
- Stopping or expansion criteria:
