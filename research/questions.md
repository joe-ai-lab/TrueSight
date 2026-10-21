# Research questions

## RQ2: Reliability under distribution shift (current focus)

Decision, 2026-10-21: the user and ChatGPT selected **Improving the Reliability of AI-Generated Image Detection under Distribution Shift**.

**Can existing AI-image detectors identify unreliable predictions when encountering unseen generators?**

Status: model-independent evaluation software and simulated software tests only; no real detector inference or research results. The [reliability protocol](reliability-protocol.md) defines scope, provisional hypotheses RH1-RH3, metrics and partition rules. RQ1 below is preserved as the earlier question and a supporting detection benchmark. No final confidence algorithm has been selected.

## RQ1: Generalization to unseen generators

**How well do existing AI-generated image detectors generalize to unseen image generators?**

Status: planning; no experiments or results.

The research direction and this question were selected by the user in discussion with ChatGPT. This record does not attribute model implementation, experimental work, or findings to the student.

### Scope and definitions

Begin with existing pretrained detectors and fully generated still images versus real photographs. Face swaps, local image edits, and video are outside the initial scope.

An unseen generator means a generator absent from the detector's documented task-specific training data. The training sources must be checked before using this designation. Unknown exposure in a pretrained backbone must be reported as a limitation; a new test dataset alone does not establish that a generator is unseen.

Reliability is the longer-term direction. The initial question concerns cross-generator performance. Threshold stability, false positives, and later controlled image modifications can extend the investigation after a reproducible baseline exists.

### Provisional hypotheses

These are expectations to test, not observations from TrueSight.

- **H1:** A detector's performance varies across generators, so an aggregate score can conceal poorly detected sources. Report per-generator results and uncertainty; consistently similar performance would weaken this expectation.
- **H2:** Performance on documented unseen generators is lower than on a held-out set from a training generator. Content and source differences may confound this comparison. Comparable or better unseen-generator performance would weaken this expectation within the evaluated scope.
- **H3:** Some apparent generalization differences reflect image format, resolution, or real-image source rather than generator identity alone. Source-stratified and matched preprocessing comparisons can investigate this possibility; an uncontrolled performance gap cannot establish it.

### Methods to investigate next

Update, 2026-10-21 (R2): the user selected CNNDetection and UniversalFakeDetect as the two baselines. A [public-data feasibility review](data-feasibility-r2.md) and [draft protocol](protocol-r2.md) now document the proposed sample and evaluation rules. The items below retain the initial investigation agenda; baseline source inspection has begun, but models and data have not been acquired and no experiment has run. Dataset selection remains conditional on provenance checks.

1. Inspect the official CNNDetection and UniversalFakeDetect implementations, pretrained weights, training descriptions, preprocessing, and score conventions. Neither baseline has been installed or evaluated for TrueSight.
2. Check available evaluation datasets for generator provenance, real-image sources, licenses, duplicates, and overlap with detector training data. No dataset has been selected or downloaded for this restart.
3. Draft a protocol with a held-out reference condition, documented unseen-generator conditions, fixed data splits, and a reproducible sampling rule. Keep any threshold selection separate from test evaluation.
4. Consider per-generator AUROC, average precision, balanced accuracy, real-image false-positive rate, and generated-image false-negative rate. Specify class balance and threshold rules before running experiments. Account for shared real images and related samples when estimating uncertainty.

Candidate official repositories for investigation:

- [CNNDetection](https://github.com/PeterWang512/CNNDetection)
- [UniversalFakeDetect](https://github.com/WisconsinAIVision/UniversalFakeDetect)

These links identify the selected baselines, not a completed reproduction or an exhaustive literature review. Record any later source-based decision in the research log.

### Intended first deliverable

A small, reproducible evaluation of existing detectors with per-generator results, explicit training-overlap limitations, and an error analysis. This is a planned deliverable; there is no evidence yet for a new detection method or a novel scientific finding.
