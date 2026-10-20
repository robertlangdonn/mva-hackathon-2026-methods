# Reproduce the exploratory public RNA analysis

This folder contains the updated report/pitch plus a standard-library-only Python
workflow. No expression matrix, patient challenge data, email, or paper PDF is bundled.
Run commands from this directory using Python 3.10 or newer (tested with 3.14.7):

```
python3 -m unittest tests.test_public_niacin_intake tests.test_public_niacin_sensitivity -v
python3 -m scripts.public_niacin_intake
python3 -m scripts.public_niacin_author_intake
python3 -m scripts.public_niacin_descriptive
python3 -m scripts.public_niacin_sensitivity
```

The two intake commands fetch three public processed GEO files, approximately
5.49 MB compressed total, and cache them locally. No raw sequencing is requested.
Subsequent runs check cached receipt hashes. Compare initial-download receipt hashes
to PUBLIC-SOURCE-RECEIPT.json before accepting a reproduction; a changed public
source requires review, not silent equivalence. The reference sensitivity-output
hash is recorded there; minor floating-point differences on another Python/platform
may require numeric comparison rather than byte equality.

Plans in docs distinguish the initial prespecified panel from post-observation
sensitivity checks. Results are descriptive, not DESeq2 significance or MVA efficacy.
All nine genes are retained. Author normalization uses the same biological samples;
agreement is not independent replication. The leave-one-pair-out analysis holds
normalization fixed. BUB1B is too sparse to assess rescue.

The six-slide pitch summarizes the hypothesis and its evidence limits.
The public RNA analysis is exploratory evidence from a different disease context,
not a demonstrated MVA rescue. The report contains the detailed qualifications.
