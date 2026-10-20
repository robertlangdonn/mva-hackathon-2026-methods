# MVA Hackathon 2026 — methods and bounded replay

Prepared by Prasad Khake for `robertlangdonn/mva-hackathon-2026-methods`.
**Reviewed methods release, updated October 20, 2026.**

## Track 2 — drug-repurposing hypothesis

Read the [report](track2/donvitocorleone_track2_report.md), watch the
[pitch video](https://youtu.be/OvHSbMbNW48), and see the
[public RNA reproduction instructions](track2/PUBLIC-ANALYSIS.md).
The proposal concerns nicotinic acid and residual BUBR1 function; it is not
demonstrated MVA efficacy or treatment advice. The Track 1 code components below
are preserved unchanged. Challenge acceptance is separate from publication.

Four immutable demonstration archives and one separately reviewed phase/splice
supplement are packaged side by side. They are independent versioned components,
not one merged Python environment. Never overlay their `scripts/` directories.

| Component | Supported scope |
|---|---|
| `code/methods.tar.gz` | Invented population semantics, CDS, conservative indel and submission-schema tests |
| `code/replay.tar.gz` | Invented intake-to-ranking with caller-supplied resources |
| `code/read_evidence.tar.gz` | Invented retained-read assessment and consolidation |
| `code/intake.tar.gz` | Invented intake and phenotype-document extraction |
| `supplement/` | Bounded source/journal/reference checks, scoped graph replay, historical comparison and offline splice-output replay |

## Verify and run

Run `python3 -I -B verify_release.py` from this directory to verify the exact outer
inventory and hashes before running a component. Use Python 3.11 or newer.
Extract each archive into its own empty directory; change into its `package/`
directory and run `python3 -I -B verify_and_test.py`. Read each component README
and environment record first. Do not run historical acquisition/alignment
controllers merely because an archive contains them as import dependencies.

From `supplement/`, run its README's isolated unittest command. All 56 supplement
tests use invented data and require only the Python standard library. Optional
real-data replay requires separately authorized local resources, tools and the
exact pinned runtime. No data acquisition, dependency installation or network
transfer is part of these recipes. Keep resulting files and process logs private.

The phase CLI requires explicit `--workspace-root`, `--alignment-data` and
`--output` arguments. It expects the documented legacy resource layout, including
historical inventories and original sources as hash-checked resources, never
imported executable code. It is not an arbitrary-dataset pipeline. The splice
CLI requires existing hash-pinned prior/control receipts and runtime resources.
See `supplement/README.md` for arguments, caps and supervision requirements.

## What was reproduced, and what was not

In a separate authorized local execution, the supplement reproduced every saved
graph edge/support count and all eight shared summary fields. The offline splice
recipe matched lead, preferred-transcript and synthetic-control predictions at
the upstream reported precision. Those controlled inputs, outputs and receipts
are NOT in this directory; synthetic tests alone do not reproduce patient results.

This is not full original raw-read-to-report reproduction. Original alignment,
historical resource acquisition/transformation, reference-protein reconstruction
and complete adjudication remain outside these recipes. Computational parity is
not independent biological replication, demonstrated phase, measured RNA,
demonstrated protein dysfunction, diagnosis or treatment advice.

## Contents, licensing and publication boundaries

The outer manifest pins every payload file. Internal manifests and original
archives are preserved byte-for-byte; `component-versions.json` identifies shared
source names and differences without merging them. Historical internal metadata
describes each snapshot's packaging state, not approval of this combined release.

One shared source filename differs: `scripts/interim_read_support.py`. The
read-evidence archive includes its scanner/CLI, while the supplement contains
only the exact same `base_at` function. Keep these versioned contexts separate;
the difference is not an instruction to replace either file.

No patient data, nomination CSV, controlled Track 1 report capsule, private receipts/logs, databases,
runtime binaries, third-party implementations or model weights are included.
CC BY 4.0 applies only to participant-owned work. Read `LICENSE.md`,
`THIRD_PARTY_NOTICES.md` and `supplement/THIRD_PARTY_NOTICES.md` for exclusions and
version-specific dependency notices. No blanket third-party rights clearance or
exhaustive privacy guarantee is claimed. The participant authorized this reviewed
release and Track 2 submission; publication alone is not a submission receipt.

## Acknowledgement and disclosure

This work was made possible through the Hackathon, organized by Sage Bionetworks
in partnership with the MVA Society, Hugging Face, and BEACON, with prize
sponsorship from AWS and Anthropic. We are deeply grateful to the child and their
family for contributing their data and story, and acknowledge their trust.
Retain this acknowledgement and recheck formal citation before publication.
Official challenge resources:
https://huggingface.co/datasets/SageBio/mva-hackathon-2026-data and
https://www.synapse.org/Synapse:syn76251147/wiki/642892 .

AI assistance: the participant reports using OpenAI Codex on a $20 plan;
historical data-sharing settings and MVA-attributable costs are unknown.
Track 2 additionally uses local Kokoro Heart synthetic narration.
