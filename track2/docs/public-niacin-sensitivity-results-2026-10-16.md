# Niacin sensitivity check: direction survives, magnitude remains fragile

The month-4 SIRT2 RNA increase survives the author-normalization check, pseudocount sensitivity and omission of any one patient pair. However, its size depends strongly on which three of the four pairs remain. This strengthens confidence in the calculation, not evidence of MVA rescue.

## Verification

Downloaded only the public author-normalized table (4,060,857 bytes), SHA256 `b46fc5fbc1e892d98f6cb9c940416c73d81d13e59f343f5c496c874481a82b64`. Total public compressed intake is now 5,485,414 bytes. No SSD, challenge data, paid compute or external writes.

Source: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE129811 . Existing raw/metadata hashes were checked before processing. Author-normalized data contain 24,878 rows, versus 58,400 raw rows. The initial exact-set check correctly stopped; an explicit schema amendment allows only a strict subset with matching IDs, symbols and sample columns. No filtering reason is inferred. All nine planned genes are present.

Across 721,462 matched gene/sample values, local normalization and the authors' values agree at relative/absolute tolerance 1e-9 (zero mismatches; largest absolute difference scaled by max(1, author value) about 4.98e-15). Therefore these are effectively the same normalization, not two independent analytical or biological confirmations.

## SIRT2 findings

- Month 4, four patient pairs: all four changes positive; median paired log2 change +0.418, about 1.34-fold with +1 pseudocount.
- Dropping one pair at a time leaves the median positive, but it ranges from +0.0237 to +0.8123 log2 (about 1.017–1.756-fold). These are sensitivity bounds, not confidence intervals. Size factors are held fixed, not refitted.
- Pseudocounts 0, 0.5 and 1 retain the positive direction; expression is high enough that this choice has little effect.
- Month 10, three patient pairs: median +0.1451; leave-one-out medians range -0.7134 to +0.5072. A durable positive response is not robustly established.
- Healthy controls, eight month-4 pairs: four positive, median +0.0432; leave-one-out medians cross zero. No formal disease-versus-control interaction test was performed.

## Full panel retained

Author-normalized patient month-4 results, +1 pseudocount. Local results agree to numerical precision. No p-values or significance claims.

| Gene | Positive pairs / 4 | Median log2 change | Leave-one-out median range |
|---|---:|---:|---:|
| BUB1B | 0 | 0.0000 | 0.0000 to 0.0000 |
| SIRT2 | 4 | +0.4180 | +0.0237 to +0.8123 |
| NAPRT | 3 | +0.5791 | +0.2035 to +0.9547 |
| NAMPT | 1 | -0.4953 | -0.6443 to -0.3463 |
| NMRK1 | 1 | -0.0787 | -0.0894 to -0.0681 |
| NMNAT1 | 0 | -0.1842 | -0.2562 to -0.1122 |
| NMNAT2 | 2 | +0.0712 | -0.1854 to +0.3279 |
| NMNAT3 | 2 | +0.0139 | -0.1320 to +0.1598 |
| CD38 | 1 | -0.2925 | -0.3814 to -0.2036 |

BUB1B, NAPRT and NMNAT2 retain the original low-count flags. BUB1B zero-pseudocount comparisons are undefined when a paired value is zero. Sparse BUB1B month-10 ratios must not be presented as rescue. The full 162 combinations (nine genes, three cohort/time comparisons, two normalization sources, three pseudocounts) are saved locally, including undefined outcomes.

## Reproduce and decision

1. `python3 -m scripts.public_niacin_author_intake` — cached hash-pinned intake; downloads only if missing.
2. `python3 -m unittest tests.test_public_niacin_intake tests.test_public_niacin_sensitivity -v`
3. `python3 -m scripts.public_niacin_sensitivity`

Output: ignored `data/cache/public-niacin-GSE129811/sensitivity-summary.json`. Twelve focused synthetic tests cover arithmetic, zeros, pairing, malformed matrices and input format. They are not biological validation.

This is post-observation sensitivity on an uncontrolled before/after dataset from another disease. It cannot establish drug causality, SIRT2 enzyme activity, BUBR1 stability, segregation rescue or pediatric safety. Do not add more analytic variants to chase a stronger signal. The useful next step is a clearly labelled exploratory appendix and a feasible cell-based test of the protein/function chain. The lab inquiry is still a draft; no email sent, scored files or recording package changed.
