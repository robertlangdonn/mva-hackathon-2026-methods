# Supplemental multi-chunk phase replay (local review only)

Python standard library only. From this directory run:
python3 -I -B -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'));sys.exit(not r.wasSuccessful())"

The CLI is python3 -m scripts.portable_phase_multichunk --contract CONTRACT --output NEW_DIRECTORY.
Use fresh controlled output directories. Never upload contracts, contexts or read outputs.
Schema phase-multichunk-v1 has complete=true, total_pairs, ordered chunks, markers,
and endpoints (two distinct marker indices). Each chunk has absolute path, sha256,
start_pairs inclusive and end_pairs exclusive. Ranges must begin at zero, be
contiguous, nonoverlapping and end at total_pairs. Duplicate underlying files and
read names across chunks are rejected, not pooled. Chunks preserve whole read groups.

Markers each have kind (snv, simple_indel, repeat_indel) and key
[contig,positive_position,REF,ALT]. Indels additionally require context (ACGT string)
and context_start (positive position). Context REF is checked; context is bound
by the contract hash, but not independently authenticated against a genome FASTA.
Method-ineligible indels fail rather than silently changing the assessor.

Compressed/decompressed aggregate cap 64 MiB each, contract 8 MB, chunks 256,
markers 500, names 50000, observed records 100000, line 64 KiB, time 120 seconds.
Hashes are checked before and after scanning, imported scientific sources pinned,
existing outputs refused. Output edge support is indexed, without read names.
Range metadata is a declared input scope, NOT a recomputed raw-pair census or
proof that a production journal is complete. A separate read-only journal adapter
is included: python3 -m scripts.phase_journal_adapter --spec SPEC --sha256 HASH
--output NEW_DIRECTORY. Its specification pins plan/scope/completion/marker files
and names the local census/download receipts, focus, sources and chunk directory.
It checks the completed receipt chain without importing controllers or cleanup.
An actual completed local journal has also been verified. This adapter does not recount
raw pairs, authenticate reference contexts, select markers, or establish phase.

For the complete saved-graph recipe use scripts.portable_phase_workflow with
--workspace-root RESOURCE_TREE --alignment-data CHUNK_DIRECTORY --output NEW_PRIVATE_DIRECTORY.
The root must contain the versioned legacy resource layout named explicitly in
verify_portable_patient_snapshot.py: historical receipts/inventories, raw VCF/index,
reference FASTA/FAI and original source files for hash checking only. Those sources
are never imported. The output must be a fresh folder under data/intermediate.
bcftools and samtools must already be installed on PATH; binaries are hashed.
No downloads/installations occur. Model weights are not used by this phase recipe.
Provenance rehashes at most 8 GB of unique input files with a cooperative 300 s guard.
Scope derivation scans at most two whole-chunk batches of 64 MiB each; scoped output
and reader limits remain 64 MiB. No partial graphs are pooled. Historical indexed
edges, both support counts and eight summary fields must match exactly.
This is legacy-layout replay, not a fresh arbitrary-dataset analysis pipeline.

Optional offline splice replay: scripts.portable_splice_replay takes --prior,
--prior-sha256, --transcripts, --transcripts-sha256 and --output. Historical
receipts name the reference/model files; preferred-transcripts.tsv must accompany
the transcript receipt. Supply an already provisioned runtime with exact receipt
versions. Nothing is installed or downloaded. Weight/code/reference hashes are
checked before/after; output must be fresh and controlled. CPU-only, two threads,
8 GB unique inputs, cooperative 300 s limit. Use an external 300 s process timeout.
Predictions and controls are compared at the upstream two-decimal precision;
protein reconstruction is not replayed. Synthetic tests do not load models.
Check third-party code/weight licenses before obtaining or redistributing them;
no third-party implementation, model weight or patient input is included here.

Tests use invented inputs only and distinguish exact same/opposite edge support,
shiftable repeats, simple indels, quality filters, conflicts, duplicate names,
missing/overlapping ranges, hash drift and refusal to overwrite.
Connectivity is NOT a parity-consistent phase solution or causality.
Pure functions are verbatim source extractions with minimal import headers;
the conservative indel module and portable readers are copied in full.
No production controllers, private data, references, model weights or binaries.
Not yet part of the frozen public release allowlist; no publication authorization.
