# Evidence grading rules

Use these labels inside Workflow Cards and the Workflow Matrix.

## Evidence strength

- **strong**: multiple independent evidence types support the claim, and the relevant data/methods are adequate for the claim.
- **medium**: evidence supports the claim, but one major validation layer, metadata element, or methodological control is limited.
- **weak**: the claim is mostly inferred from one analysis type, has incomplete metadata, or lacks validation.
- **unable to determine**: available text does not provide enough information.

## Evidence type labels

- `atlas evidence`: clustering, annotation, marker support, cell-state definition.
- `lineage evidence`: trajectory, RNA velocity, PAGA, pseudotime, fate inference.
- `regulatory evidence`: GRN, regulon, motif, TF activity.
- `communication evidence`: ligand-receptor or niche analysis.
- `spatial evidence`: spatial transcriptomics, neighborhood, tissue location.
- `clinical evidence`: survival, response, deconvolution, external clinical cohort.
- `experimental evidence`: perturbation, in vitro, mouse model, flow, imaging.

## Caution labels

- `hypothesis-generating`: common for communication, trajectory, and GRN modules unless validated.
- `sample-level risk`: cell-level statistics may not account for patient/sample replication.
- `metadata risk`: missing treatment, tissue, patient, platform, or batch labels.
- `overcorrection risk`: integration may remove biological differences.
- `annotation risk`: reference or marker choice may force cells into old labels.
