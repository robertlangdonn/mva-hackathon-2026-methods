# Post-observation sensitivity specification

This follows the observed SIRT2 month-4 increase and is not an independent or confirmatory analysis. No change to the fixed nine-gene panel, pairing or disease groups.

Retrieve only the author-deposited GSE129811_AWVM29samples.DESeq.normCounts.csv.gz (advertised about 3.9 MB), within the existing 10 MiB per-file/25 MiB total compressed caps. Verify exact stable gene IDs and sample mapping against raw counts before comparison. Preserve the original intake receipt; record a separate hash receipt.

Compare author normalization to locally reconstructed median-of-ratios normalization. Across both methods report all panel month-4 and month-10 complete-pair medians, positive-pair counts and ranges of leave-one-pair-out medians, holding size factors fixed. This deletion check tests individual-pair influence, not normalization refits or uncertainty intervals. Repeat pseudocounts 0, 0.5 and 1; mark zero-pseudocount undefined whenever any paired value is zero. No tests/p-values or post-hoc gene-set searches. If matrices are effectively identical, report computational agreement, not independent biological evidence.

Do not promote sparse BUB1B ratios. Report adverse/opposite panel directions. Author normalization may be a transformation of the exact same counts; no causal effect or protein activity can be inferred. Preserve scored Track 1 and Track 2 recording package.

Schema amendment before author effects: the author table has 24,878 rows, a strict subset of 58,400 raw rows, with identical 29 sample columns. Of 33,522 omitted rows, 21,276 are all zero and 12,246 have at least one positive count. Filtering criteria are not established by this inspection. All nine panel genes remain. Compare exactly matched stable IDs/symbols in the shared subset; reject novel/duplicate IDs, symbol mismatches or missing panel members. Retain original all-positive raw-gene normalization rather than silently change its universe.
