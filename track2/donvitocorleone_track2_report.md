# Testing nicotinic acid for restoration of usable BUBR1 function

**Participant:** Prasad Khake · **Hugging Face:** donvitocorleone  
**Track:** 2 — Drug Repurposing · **Version:** submission package, October 20, 2026  
**Status:** Final submission report. Hypothesis for laboratory investigation, not treatment advice.

## Executive summary

I propose investigating **nicotinic acid (niacin)** as a means of supporting
residual BUBR1 function through NAD-dependent regulation. The hypothesis joins
three observations: nicotinic acid can increase cellular NAD through NAPRT;
NAD/SIRT2 can influence BUBR1 stability in experimental models; and increasing
functional BUBR1 can correct defects in some MVA-derived cells. These observations
come from different studies and interventions. Their connection in the relevant
disease context remains untested. [1–4,14]

The proposed outcome is better chromosome segregation with preserved cell output,
not simply more NAD, more BUBR1 or fewer abnormal surviving cells. A staged assay
would test precursor utilization, intracellular target engagement, BUBR1 response
and function, stopping when the causal chain fails. Prescription nicotinic acid
has approved uses outside MVA, but approval does not establish efficacy, exposure
adequacy or safety for this application. [5]

The contribution is a falsifiable repurposing rationale with explicit alternatives
and failure criteria. No MVA drug efficacy, exact-allele functional rescue or
clinical dosing is claimed.

## 1. Disease mechanism and relevance

BUB1B encodes BUBR1, which contributes to the spindle checkpoint and stable
chromosome attachment during division. Published MVA work distinguishes variants
that reduce protein abundance from variants that impair function despite protein
being present. A drug that preserves an intrinsically defective protein may not
restore chromosome fidelity. [4]

The associated Track 1 analysis prioritized BUB1B. Its nomination is a starting
point for this mechanism hypothesis, not evidence of drug responsiveness. Phase
and the exact missense allele's functional behavior remain unresolved. This report
does not reproduce controlled variant coordinates, genotypes, read sequences or
patient-scale derivatives. It assumes neither NAD deficiency nor a demonstrated
stabilization-responsive allele in the child.

The working mechanism is reduced usable BUBR1 activity, consistent with a
loss-of-function framework. Whether the relevant bottleneck is abundance,
localization, checkpoint control or another function must be experimentally
distinguished before interpreting a response.

## 2. Candidate identity and evidence ladder

The candidate is **nicotinic acid**, not nicotinamide, nicotinamide riboside or
nicotinamide mononucleotide (NMN). The regulatory reference is the US prescription
niacin extended-release tablet listed under ANDA203899, repackaged by Golden State
Medical Supply (NDC 51407-267-90 and 51407-268-90; source NDCs 62175-320 and
62175-322). This anchors an existing drug product, not a purchase or dosing
recommendation. Equivalence to the human pilot's preparation remains unverified. [5]

The pilot's resource table identifies Sundown Naturals SDN-29505 and Nature's
Bounty NRT-05800 time-release products. These identities resolve the trial-product
lookup, but do not establish equivalence to the prescription reference. [3]

| Link | What the evidence supports | What it does not establish |
|---|---|---|
| Nicotinic acid → NAD | NAPRT-dependent NAD elevation in tested human cells [1] | Engagement in every tissue or disease model |
| NAD/SIRT2 → BUBR1 | Separate NMN and genetic SIRT2 experiments support regulation of abundance [2] | Nicotinic-acid rescue of MVA chromosome division |
| Functional BUBR1 → rescue | Genetic restoration in published MVA cell experiments [4,14] | Rescue by stabilizing any particular missense protein |
| Human translation | NAD restoration in an adult mitochondrial-myopathy pilot [3] | Pediatric MVA efficacy, safety or formulation equivalence |

In the BUBR1 study, NMN increased NAD in both SIRT2-competent and deficient cells,
while the BUBR1 response was largely SIRT2-dependent. The lifespan experiment used
genetic SIRT2 overexpression; it was not a demonstration of lifespan extension by
the short NMN treatment. These distinctions prevent a drug claim from being
inferred from a genetic intervention. [2]

Review of the supplied supplements strengthens the enzyme mechanism: active versus
inactive and recombinant SIRT2 controls support direct deacetylation, while
cell-cycle controls address gross redistribution. They do not establish repaired
chromosome segregation. The genetic intervention did not normalize small body size
or several ECG abnormalities. Published discussion and peer-review responses
acknowledge other SIRT2 targets and residual NMN effects without SIRT2, preventing
exclusive attribution of benefit to BUBR1. [2, supplementary figures S1–S6 and
public peer-review file]

The human niacin study was small, open-label and non-randomized; both patients and
healthy controls received intervention. Several functional analyses included five
patients and eight controls. Increased blood NAD did not imply increased NAD in
healthy muscle. Hematologic changes and the absence of an untreated disease arm
limit interpretation. [3,6]

## 3. Exposure and safety limitations

The human pilot used slow-release nicotinic acid. The investigators' clarification
does not establish equivalence to a particular current prescription product. [7]
The reviewed prescription label describes variable, saturable first-pass
metabolism and lacks pediatric pharmacokinetic evidence for its stated pediatric
population. An oral amount cannot therefore be linearly translated into culture
concentration or intracellular NAD availability. [5]

The initial cell experiments would use chemically defined nicotinic acid with
matched vehicle, rather than crushed extended-release tablets. This tests the
active molecule, not the oral release profile. Translation would require measured
concentration-response and intracellular engagement, followed by comparison with
product-specific exposure data. A constant culture exposure cannot stand in for
an oral concentration-time profile.

No effective concentration for nicotinic-acid-mediated BUBR1 rescue has been
established here. Consequently there is no defensible clinical efficacy margin
or dosing schedule in this proposal. Hepatic, hematologic and metabolic liabilities
must be considered, and MVA-specific tumor-predisposition safety remains unknown.
Being a vitamin does not make pharmacological use harmless. [3,5,7]

Counterevidence makes safety a mechanistic question. In high-glucose mouse islets,
NMN reduced proliferation and SIRT2 inhibition partly reversed that effect. This
does not show niacin toxicity in MVA, but cautions against assuming that NAD/SIRT2
enhancement preserves growth in every tissue. [15] Nicotinic acid also protected
tumors from NAMPT inhibition in one xenograft study, whereas a later pediatric
rhabdomyosarcoma study reported preserved tumor regression in its NAPRT-deficient
models. These opposing results concern particular cancer-treatment models, not
proof that niacin causes cancer. They require context-specific tumor and
drug-interaction evaluation before translation. [16,17]

## 4. Proposed validation and decision gates

These experiments are proposed, not completed. Laboratory access, model availability,
ethics approvals and resources are not represented as secured.

**Stage A — establish an interpretable model.** Demonstrate a reproducible division
defect and a functional WT-restoration control. Include vehicle, WT plus candidate,
disease-model plus candidate and an endpoint-appropriate published MVA control.
Use expression-matched comparisons to examine intrinsic function alongside a
physiologically constrained expression context that preserves instability effects.
An isolated construct cannot reproduce the complete biallelic background.
Measure baseline NAD and compare disease and matched WT cells; a normal baseline
does not exclude pharmacological engagement, but invalidates a deficiency-correction
claim unless deficiency is demonstrated. Verify that WT restoration works before
interpreting failure of the candidate.

**Stage B — verify precursor engagement.** Measure intracellular NAD and precursor
utilization; assess NAPRT competence. Protein expression alone is not a metabolic
flux measurement. Failure to raise NAD stops the proposed chain in that model;
it does not justify arbitrary exposure escalation or prove all NAD strategies fail.

**Stage C — test the BUBR1 bridge.** Measure abundance, turnover and kinetochore
localization with and without SIRT2 perturbation. Analyze baseline-adjusted effects:
SIRT2 perturbation can itself impair division. A NAD response without a useful
BUBR1 response does not support the restoration mechanism.
Include catalytic-activity controls and orthogonal turnover measurements where
feasible. SIRT2 dependence alone does not prove BUBR1 mediates functional benefit:
use appropriately controlled BUBR1 perturbation/restoration comparisons, accounting
for their baseline division defects, before making that stronger causal claim.

**Stage D — require functional benefit.** Use segregation errors per observed
division as the proposed primary endpoint. Report mitotic duration, checkpoint
activation and recovery, viability, proliferation and absolute viable-cell output
together. Predefine exposure range, effect threshold and independent replicate
number from baseline variance and laboratory expertise before inspecting drug
responses. Blind scoring, randomize conditions and treat cultures/biological
replicates—not individual cells from one well—as the appropriate independent units.

| Result | Interpretation and decision |
|---|---|
| More NAD/BUBR1, unchanged segregation | Molecular response only; restoration hypothesis not supported |
| Fewer abnormal cells with more death or fewer divisions | Possible selection/cytostasis; not repaired division |
| Better metabolism without BUBR1 function | Consider a separately tested compensation mechanism |
| Better segregation with preserved output and checkpoint exit | Advance to independent replication and relevant tissue models |
| WT impairment or compromised renewal | Reject or sharply restrict the experimental approach |

**Stage E — tissue and tumor-safety qualification.** After replicated functional
benefit, require relevant tissue renewal and longer-term proliferation/selection
assessment, with specialist-designed tumor-context and treatment-interaction
studies. Do not infer cancer safety from short-term cell viability, NAPRT staining
alone or the adult myopathy study, which excluded malignancy requiring continuous
treatment. [3,15–17] No such safety experiment has been performed here.

The accompanying [experimental analysis plan](track2-experiment-analysis-plan.md)
specifies the comparison set, denominator safeguards, biological replicate unit
and confirmatory decision rules. Numerical effect thresholds and sample sizes
must be fixed with the laboratory using baseline data before efficacy testing.

## 5. Alternatives and negative evidence

**Sirolimus:** a downstream comparator only, not a combination proposal. One
published BUBR1 mouse-model comparison found differing muscle mTORC1 signaling
despite similarly reduced BUBR1 levels. Pathway hyperactivity must be measured,
not assumed. [8] A separate paper mentions preliminary rapamycin non-benefit as
unpublished data: retain it as a low-detail warning, not a definitive trial. [9]
Approved sirolimus carries immune and wound-healing liabilities. [10]

**Arimoclomol:** no direct BUBR1 rescue was established
in this bounded review. Positive and negative non-MVA cell studies disagree across
contexts. Target engagement, protein specificity and achievable exposure remain
unresolved. [11,12]

**Broad HDAC inhibition and global PP2A activation:** site, timing and localization
matter. Sustained BUBR1 acetylation can prevent mitotic exit; artificial kinetochore
PP2A recruitment is not equivalent to systemic phosphatase activation. [13,14]

These alternatives explain the provisional prioritization, not an exhaustive
ranking of all approved drugs. No first-in-field or unique-candidate claim is made.

SIRT2 overexpression also failed to improve health or lifespan in a separate
wild-type mouse study. This limits generalization from hypomorphic models without
directly refuting an MVA-specific hypothesis. [18] Nicotinic acid remains a
conditional first laboratory test because its proposed bridge is experimentally
separable. Sirolimus becomes more relevant only if abnormal mTORC1 activity is
demonstrated and functional BUBR1 restoration is not achieved; switching would
require a separately defined compensation endpoint and safety review. Neither
candidate has demonstrated MVA drug efficacy in this project.

## 6. Impact, feasibility and reproducibility

If supported, this approach could justify further work on stabilization-responsive
BUBR1 disease contexts. It may fail where residual protein lacks useful function,
precursor metabolism is insufficient or the relevant tissue does not respond.
Generalization requires testing rather than gene-name matching.

The proposed sequence spends resources on basic model validity and engagement
before complex tissue studies. Commercial availability of a molecule does not
establish experimental feasibility, clinical affordability or pediatric suitability.
No wet-lab budget or clinical implementation estimate is claimed.

This is a hypothesis-driven literature synthesis with an exploratory reanalysis
of an existing public RNA dataset, not a systematic review or a newly generated
drug-response dataset. Public primary papers, official labels and the trial
registry were prioritized. Retrieval depth varies: some sources were reviewed as
indexed Results/Methods or abstracts rather than complete supplements. Our
source coverage now includes all supplied North 2014 supplementary figures and its
public peer-review history; this is a literature audit, not raw-data reanalysis.
Reproducible documentation consists of the source-linked evidence records, candidate comparison
and proposed analysis gates. There is no executable experiment that reproduces an
MVA drug response because no such response has been measured in this work.
The exploratory appendix below concerns mitochondrial-myopathy muscle, not MVA;
it neither establishes the proposed protein mechanism nor changes the nomination.
The accompanying [claim-to-evidence audit](track2-claim-evidence-audit.md) records
the source-review depth and limits for each major claim.

The existing methods repository is
https://github.com/robertlangdonn/mva-hackathon-2026-methods . The accompanying `track2/` release contains the report, editable pitch, narration, claim audit, experiment plan, and public RNA scripts, tests and source fingerprints. No challenge patient data, private correspondence or third-party paper PDFs are included. The repository manifest pins the released bytes; publication and submission receipts are tracked separately.

## 7. AI, resources and disclosure

Pitch video: https://youtu.be/OvHSbMbNW48 . The participant uploaded the video
to YouTube; its public metadata was accessible without authentication on
October 20, 2026. Local rendered duration is 176.02 seconds. The video uses
synthetic Kokoro Heart narration generated locally, not the participant's voice.

OpenAI Codex assisted literature discovery, evidence comparison, public-data
analysis code and drafting.
The participant reports a “Codex $20 plan”; exact tier/billing details and historical
data-sharing/training settings are unknown. No other hosted AI service was reported.
Local Kokoro text-to-speech was subsequently used for the pitch narration.
MVA-attributable costs are unknown, not zero. This Track 2 synthesis used public
sources and limited mechanism summaries, not raw patient data in external searches.
This statement does not retrospectively certify every historical service setting.

No external laboratory has committed to conduct the proposed experiments. Private
correspondence is not quoted or represented as endorsement. I retain responsibility
for reviewing the evidence and final submission.

## 8. Methods-template responses

These responses follow the organizer's Track 2 methods worksheet, rows 7–17.

- **Participant:** Prasad Khake (donvitocorleone).
- **Approach:** mechanism-led comparison of public literature and official drug
  information, followed by a staged, falsifiable experimental proposal (sections
  1–6). No drug-response prediction model or wet-lab experiment was run.
- **AI disclosure:** see section 7. Historical settings remain unknown.
- **Identification and curation:** LLM-assisted searches and qualitative literature
  comparison, not an automated drug-target ranking. Candidate selection includes
  interpretive curation. The participant approved release and submission. No independent expert
  has validated this candidate nomination.
- **Review detail:** separate intervention, model, endpoint and evidence strength;
  retain contradictory findings and exposure limitations. This is a bounded review,
  not a systematic search with a complete screened-paper denominator.
- **Sources:** public primary publications, PubMed/PMC, ClinicalTrials.gov,
  DailyMed and an investigator FAQ (references below). No proprietary drug database
  was used. Controlled challenge analysis supplied the BUB1B starting context;
  this is not a claim that the entire project used only public data. No raw patient
  data were used for external literature searches.
- **Mechanism:** provisional reduced usable BUBR1 activity, with abundance and
  intrinsic-function defects distinguished. Exact-allele response remains untested.
- **Effort:** total person-hours, model runtime and MVA-attributable cost were not
  reliably metered. They are unknown, not zero. No new wet-lab work is included.

### Method abstract (under 500 words)

I developed a mechanism-led research proposal to test nicotinic acid for residual
BUBR1 function in MVA-related models. LLM-assisted public-literature discovery and
qualitative comparison linked precursor utilization, NAD-dependent regulation and
chromosome-division endpoints. I distinguished experiments using nicotinic acid,
NMN and genetic SIRT2 manipulation instead of treating them as equivalent evidence.
Official labeling anchors an approved prescription product but does not establish
MVA exposure adequacy. Alternative mechanisms and negative findings inform candidate
prioritization. Proposed validation first establishes model validity and precursor
engagement, then tests BUBR1 response and segregation errors per division with
viability, checkpoint recovery and cell output. The approach makes failure criteria
explicit and separates molecular response from functional rescue. Its limitations
include incomplete source retrieval, unresolved allele responsiveness, unproven
formulation equivalence and the absence of MVA drug-response experiments. The
output is a testable repurposing hypothesis, not evidence of therapeutic benefit.

## Exploratory appendix: public niacin-response RNA

An exploratory reanalysis of the processed counts and metadata deposited in
[GSE129811](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE129811), associated
with Pirinen et al. [3], examined a fixed nine-gene panel: BUB1B, SIRT2, NAPRT,
NAMPT, NMRK1, NMNAT1, NMNAT2, NMNAT3 and CD38. This reused published data; it is
not independent replication or a new MVA experiment. The panel and descriptive
method were recorded before expression effects were inspected. Sensitivity
checks were specified after the initial results and are labelled post-observation.

All 29 RNA samples mapped to 13 participants. Complete baseline-to-month-4 pairs
were available for four mitochondrial-myopathy patients and eight healthy controls;
only three patient baseline-to-month-10 pairs were available. Both groups received
niacin; healthy controls are not an untreated longitudinal comparison. Missing
baselines were not imputed. Median-of-ratios normalization used 15,019 genes with
positive counts across samples. No count-model significance tests were performed.

The median paired log2 changes at month 4 in patients, using a fixed +1 normalized
count pseudocount, were:

| Gene | Median log2 change | Positive pairs / 4 |
|---|---:|---:|
| BUB1B | 0.0000 | 0 |
| SIRT2 | +0.4180 | 4 |
| NAPRT | +0.5791 | 3 |
| NAMPT | -0.4953 | 1 |
| NMRK1 | -0.0787 | 1 |
| NMNAT1 | -0.1842 | 0 |
| NMNAT2 | +0.0712 | 2 |
| NMNAT3 | +0.0139 | 2 |
| CD38 | -0.2925 | 1 |

SIRT2 increased in all four month-4 patient pairs (median approximately 1.34-fold).
Holding normalization fixed and omitting each pair in turn kept the median positive,
but yielded log2 changes from +0.0237 to +0.8123: magnitude is fragile. These bounds
are not confidence intervals. Pseudocounts 0, 0.5 and 1 retained this direction.
The month-10 SIRT2 result was less stable: leave-one-pair-out medians crossed zero.
Healthy-control month-4 changes were mixed (four of eight positive); no formal
between-group interaction was tested. BUB1B RNA was too sparse to evaluate rescue;
NAPRT and NMNAT2 also had low-count observations. Opposing panel directions are
retained rather than interpreting the entire pathway as uniformly activated.

The author-normalized table retained 24,878 of 58,400 raw rows. All nine panel
genes and all sample columns were matched explicitly. Across 721,462 shared
values, reconstructed normalization agreed with the authors' values to 1e-9
relative/absolute tolerance. This validates computational agreement on the same
samples, not independent biology or robustness to a distinct normalization method.

This small, nonrandomized before/after dataset cannot separate treatment from time
or other confounders. SIRT2 RNA is not SIRT2 activity; neither RNA observation
establishes BUBR1 protein stabilization, chromosome-segregation rescue or pediatric
safety. The finding supports prioritizing an enzyme/protein/function experiment,
not claiming that the proposed therapeutic chain has been demonstrated.

## References

1. Hara et al. 2007. NAPRT and nicotinic-acid-mediated NAD elevation. https://doi.org/10.1074/jbc.M610357200
2. North et al. 2014. SIRT2 and BUBR1 stability. https://pmc.ncbi.nlm.nih.gov/articles/PMC4194088/
3. Pirinen et al. 2020. Niacin in mitochondrial myopathy. https://doi.org/10.1016/j.cmet.2020.04.008
4. Suijkerbuijk et al. 2010. Molecular causes of BUBR1 dysfunction in MVA. https://pmc.ncbi.nlm.nih.gov/articles/PMC2887387/
5. Niacin extended-release prescribing information. https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=8eff9205-84ac-e69d-e053-2995a90aad4b
6. NiaMIT trial registry. https://clinicaltrials.gov/study/NCT03973203
7. Investigators' niacin FAQ. https://www.helsinki.fi/en/researchgroups/mitochondrial-medicine/faq-niacin
8. BUBR1 allelic effects in MVA-related mouse models. https://www.jci.org/articles/view/126863
9. p21 in BubR1 progeroid mice. https://pmc.ncbi.nlm.nih.gov/articles/PMC3785294/
10. Sirolimus prescribing information. https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=2e6130e5-fa94-dcf8-605c-817bf396e93d
11. Fog et al. 2018. Arimoclomol and glucocerebrosidase. https://pmc.ncbi.nlm.nih.gov/articles/PMC6306395/
12. Pipalia et al. 2021. HSP90 inhibition and NPC1 models. https://pubmed.ncbi.nlm.nih.gov/34481829/
13. Park et al. 2017. BUBR1 deacetylation and checkpoint silencing. https://pubmed.ncbi.nlm.nih.gov/28985013/
14. Xu et al. 2013. BUBR1 recruitment of PP2A-B56. https://pmc.ncbi.nlm.nih.gov/articles/PMC3654266/
15. Wortham et al. 2025. SIRT2 and adaptive beta-cell proliferation. https://doi.org/10.1172/JCI187020
16. O'Brien et al. 2013. Nicotinic acid rescue of NAMPT-inhibited tumor models. https://doi.org/10.1593/neo.131718
17. Kim et al. 2026. NAPRT in pediatric rhabdomyosarcoma and NAMPT inhibition. https://doi.org/10.1158/1535-7163.MCT-25-0619
18. Wu et al. 2023. SIRT2 overexpression and wild-type mouse health/lifespan. https://doi.org/10.1111/acel.14027
