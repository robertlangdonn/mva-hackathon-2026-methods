# Public niacin reanalysis: preliminary descriptive results

The public muscle RNA-seq data are usable for a small paired descriptive analysis, but poorly suited to testing BUBR1 rescue. SIRT2 RNA increased in all four available patient month-4 pairs; BUB1B RNA was extremely sparse. These are exploratory observations in mitochondrial myopathy, not MVA efficacy evidence. The submitted Track 1 files and Track 2 recording package have not been changed.

## Provenance and reproducibility

- Plan: `docs/public-niacin-analysis-plan-2026-10-16.md`, recorded before expression effects were inspected.
- Intake: `python3 -m scripts.public_niacin_intake`
- Analysis: `python3 -m scripts.public_niacin_descriptive`
- Tests: `python3 -m unittest tests.test_public_niacin_intake -v`
- Public source: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE129811
- Cached inputs/receipt/output: ignored `data/cache/public-niacin-GSE129811/` on internal disk. No SSD or challenge-patient data used.
- Metadata gzip: 5,116 bytes, SHA256 `f4389d301e7e861b296624530e5bb8daa8c7e5492c1fa86f1d2faf85eb090da8`.
- Raw-count gzip: 1,419,441 bytes, SHA256 `d09334fd7cae194d1fac02ddbd44c13aeb47f597734097c502f86032847629cc`.

All 29 count columns mapped uniquely to metadata; 58,400 rows validated for unique IDs and nonnegative integer counts. Gene symbols for all nine prespecified genes were unique. There are 13 participants: eight healthy controls and five mitochondrial-myopathy patients. Only four patients have baseline RNA samples; month-10 complete-pair count is three. No imputation. Metadata treatment label "control" at baseline is not an untreated longitudinal control arm.

## Full prespecified panel

Values are median paired log2 changes of normalized counts with a fixed +1 pseudocount. They are not statistical significance estimates. Normalization uses 15,019 positive-count genes, median-of-ratios; size factors span 0.7734–1.3759. This is not a fitted DESeq2 analysis. A low-count flag means at least one sample has fewer than 10 raw counts, across the whole dataset.

| Gene | Healthy month 4 (8 pairs) | Patient month 4 (4 pairs) | Patient month 10 (3 pairs) | Low-count flag |
|---|---:|---:|---:|---|
| BUB1B | 0.0000 | 0.0000 | +1.7997 | Yes — sparse, do not interpret as rescue |
| SIRT2 | +0.0432 | +0.4180 | +0.1451 | No |
| NAPRT | +0.0514 | +0.5791 | +0.4599 | Yes |
| NAMPT | -0.0235 | -0.4953 | -0.6815 | No |
| NMRK1 | +0.0130 | -0.0787 | -0.1685 | No |
| NMNAT1 | -0.0423 | -0.1842 | -0.2357 | No |
| NMNAT2 | -1.4338 | +0.0712 | +0.6942 | Yes |
| NMNAT3 | -0.1236 | +0.0139 | -0.1639 | No |
| CD38 | -0.0015 | -0.2925 | -0.1587 | No |

SIRT2 increases in 4/4 patient month-4 pairs, 2/3 patient month-10 pairs and 4/8 healthy month-4 pairs. The month-4 median log2 change corresponds to approximately 1.34-fold on the pseudocount-adjusted scale. This is a hypothesis-relevant RNA observation, not an assay of SIRT2 activity. Other panel genes do not show a uniform upward pattern. All results are retained, not just SIRT2.

BUB1B normalized baseline and month-4 medians are both zero in patients. Its apparent month-10 fold change is driven by very small counts (post median about 2.48), making it a poor mechanistic endpoint. A protein-stability mechanism does not require increased BUB1B transcription, so this also does not refute that mechanism.

## Decision and remaining checks

- Do not promote the drug nomination or alter the submission based on these descriptive results alone.
- Next useful computational check: compare normalization with the authors' deposited normalized matrix and assess whether SIRT2's direction is robust to reasonable normalization and leave-one-pair-out summaries. Label this post-observation sensitivity analysis, not independent replication.
- A formal count model would require explicit design/dependency validation and multiple-testing control; the four-pair disease group remains small. No p-values claimed here.
- Do not download or combine GSE134781 yet: three-month monoallelic mouse muscle is not a matched biallelic-MVA counterpart. A cross-species signature score would not bridge the function gap.
- Higher-value biological follow-up is an existing cell model measuring target engagement, BUBR1 protein and segregation errors alongside proliferation/arrest/death. Lab feasibility email drafted separately, not sent.
- Public muscle RNA cannot establish NAD restoration in the child's relevant tissues, segregation rescue, safety or a useful clinical dose. Nonrandomized before/after changes may reflect time or other confounders.

No paid compute, uploads, submission changes or external messages. Approximately 1.43 MB downloaded. Cached reruns verify source hashes and need no network.
