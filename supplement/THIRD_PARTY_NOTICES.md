# Supplemental phase/splice package — local candidate

Participant attribution: Prasad Khake. CC BY 4.0 applies only to participant-owned
code and documentation, not external tools, scientific resources or model weights.
No publication or submission is authorized by preparing these files.

This directory contains Python implementation, invented tests and documentation.
It does not contain controlled challenge data, patient outputs, reference genomes,
original VCFs, runtime environments, binaries, third-party source code or weights.
Do not add the surrounding workspace, private manifests, logs or replay results.
Synthetic fixture values are not patient-derived examples.

## External dependencies and version-specific terms

- SpliceAI 1.3.1: the installed metadata and the tagged upstream source license
  identify GPLv3. See https://github.com/Illumina/SpliceAI/blob/v1.3.1/LICENSE
  and https://pypi.org/project/spliceai/1.3.1/ . Its current default-branch license
  differs (PolyForm Strict source; CC BY-NC models):
  https://github.com/Illumina/SpliceAI/blob/master/LICENSE . Do not substitute
  current terms for an old artifact, infer a blanket model-weight license from
  package metadata, or relicense any dependency under participant CC BY 4.0.
  No dependency or weight redistribution is proposed here. Any future combined
  distribution or different use needs a separate version-specific rights review.
- Cite Jaganathan et al., Cell (2019), https://doi.org/10.1016/j.cell.2018.12.015 .
  The replay imports an independently installed runtime; supplied helper functions
  are participant orchestration/parsers, not copied SpliceAI implementations.
- Existing replay environment: TensorFlow 2.15.1, Keras 2.15.0, NumPy 1.26.4,
  pysam 0.24.1, pyfaidx 0.9.0.4. Each retains its own terms. None is bundled.
- bcftools and samtools must already be installed. The phase recipe hashes their
  binaries and invokes local query/faidx commands; it does not supply binaries.
- Ensembl 116 reference and annotation are external resources. Acknowledge Ensembl
  and retain resource provenance; see
  https://www.ensembl.org/about/articles/ensembl-content-disclaimer .

## Claim and privacy limits

Exact historical graph and rounded splice-output reproduction is not independent
biological replication, measured RNA, clinical sensitivity, demonstrated phase or
demonstrated protein dysfunction. Original raw-read alignment, historical resource
acquisition, protein reconstruction and complete adjudication are not reproduced
by these recipes. The phase entry point requires the stated legacy resource layout.

The controlled outputs must remain local. CLI error suppression is not a guarantee
that an external library can never log sensitive context; retain process logs
privately. Run inference offline with external time/memory supervision.
These notices are scoped documentation, not a legal opinion or exhaustive rights
clearance. Hash provenance establishes byte identity, not independent authorship.
