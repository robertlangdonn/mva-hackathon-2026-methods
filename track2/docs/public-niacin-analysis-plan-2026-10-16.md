# Public niacin RNA-seq: prespecified feasibility and analysis

Recorded before inspecting expression effects, 2026-10-16. This is an exploratory reanalysis of a known published result, not independent replication or a blinded validation.

## Scope and caps

GSE129811 processed raw count table and GEO family metadata only. Public downloads <=25 MiB total compressed, each <=10 MiB; decompressed input <=100 MiB each. Internal disk only; no raw sequencing, patient challenge data, SSD access, paid computation or external messages. Pin downloaded bytes by SHA256. Metadata must reconcile to count columns before any inference.

## Questions and gates

1. Can treatment visits be paired within participants? Distinguish mitochondrial-myopathy patients from healthy controls and month 4 from month 10. Do not treat repeated biopsies as independent people. Print only aggregate cohort/schema summaries.
2. If mapping is complete, estimate within-person month-4 expression changes separately in each group. Month-10 patient changes are secondary. These are treated-before/after comparisons, not randomized treatment effects. No untreated disease arm means time, biopsy and other confounding remain.
3. Preselected narrow gene panel: BUB1B, SIRT2, NAPRT, NAMPT, NMRK1, NMNAT1, NMNAT2, NMNAT3, CD38. Resolve stable gene identifiers from public annotation; fail closed on ambiguous mappings. Inspect baseline detectability before ratios. Use all genes for normalization, never only the panel. Raw-count differential expression requires a validated count model; do not call ordinary fold-change plots differential expression.
4. Report all panel results including null/opposite directions, descriptive paired effects and sample counts. Small cohorts and prior pathway knowledge limit discovery claims. No post-hoc gene-set shopping. If formal tests are subsequently justified, specify the model and multiplicity correction before running them.
5. RNA changes cannot establish NAD concentrations, SIRT2 enzyme activity, BUBR1 protein stability, chromosome-segregation rescue or efficacy in MVA. Unchanged BUB1B RNA would not refute a protein-stability mechanism.

## Mouse comparator gate

### Descriptive analysis specification (before effects)

Use median-of-ratios size factors from all strictly positive, non-summary gene rows, with per-gene geometric means across the 29 samples. This is a descriptive normalization, not a DESeq2 model fit. Verify nonnegative integer counts, unique stable IDs, one-to-one sample mapping and unique panel symbols. For each panel gene, report normalized-count medians by visit and median within-participant log2((post+1)/(pre+1)), including the fraction of pairs with positive change. Pseudocount is fixed at one normalized count. Flag any panel with raw counts below 10 in any sample; show those observations but do not promote low-count ratios as convincing support. No p-values, significance labels or formal efficacy inference. Patient month-10 versus baseline uses complete pairs only; exclude missing baseline rather than impute it.

GSE134781 concerns three-month monoallelic mouse skeletal muscle. It is not a direct biallelic MVA patient comparator. Do not compute a pooled or cross-species "rescue score" merely because both studies use muscle. Require genotype/age/tissue/control/design reconciliation and prespecified ortholog mapping first. Defer its download until the human feasibility check is resolved.

## Sources

- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE129811
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE134781
- https://pmc.ncbi.nlm.nih.gov/articles/PMC6934189/

Published paper/resource-table accession discrepancies must be resolved using the GEO study title and study metadata, not guessed accession similarity.
