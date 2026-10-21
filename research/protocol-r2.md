# R2 draft protocol: Cross-generator detector evaluation

Version: 0.2, 2026-10-21. Status: **approved in principle; acquisition and execution pending; no runs or results**. This revision adds an 80-image technical trial before the 600-image exploratory main experiment. The user selected CNNDetection and UniversalFakeDetect as the Phase 1 baselines. Data selection remains conditional on the [feasibility checks](data-feasibility-r2.md). No full archive download is authorized at this stage.

## Question and intended inference

[RQ1](questions.md): How well do existing AI-generated image detectors generalize to unseen image generators?

Estimate each fixed detector's discrimination and error rates on specified public subsets. Test H1 descriptively across conditions. Assess H2 only if a genuinely held-out seen-generator reference can be established. H3 is a limitation to investigate, not a causal conclusion this pilot can settle. One GAN and two diffusion-family unseen candidates do not support a population-level claim about all generators or an architecture-only comparison.

## Conditions and sample accounting

Use samples traceable to AIGIBench's public **test** release at the revision recorded in the feasibility note. Investigate selective acquisition before any transfer; do not download the full 19.46 GB archive collection now. No task training, fine-tuning, calibration fitting, or synthetic image collection is planned.

### Stage A: Technical trial (80 images)

Use the four sources below, with **10 real photographs and 10 generated images per source**: 40 real and 40 generated images. Its sole purpose is to verify decoding, labels, per-detector score semantics, preprocessing, manifest handling, output persistence, and error handling. Any numerical output is a diagnostic, not a performance estimate, detector ranking, or research finding. The trial has not been run.

Use the same score-blind eligibility and deterministic selection rules as the main experiment, but freeze a separate `technical_trial` manifest first. Exclude these images and all identified related content groups from the main pool before selecting its manifest. Do not tune a threshold on the trial. Correct implementation faults with a dated record; any scientific protocol change must precede main-experiment scoring. A successful trial establishes pipeline functionality only.

### Stage B: Exploratory main experiment (600 images)

| Condition | Generator status relative to the selected original checkpoints | Real | Generated |
| --- | --- | ---: | ---: |
| ProGAN | Seen generator; sample independence pending | 75 | 75 |
| StyleGAN3 | Candidate unseen GAN | 75 | 75 |
| GLIDE | Candidate unseen older diffusion model | 75 | 75 |
| FLUX.1-dev | Candidate unseen relatively newer diffusion-family model | 75 | 75 |
| Target | Four conditions | 300 | 300 |

The target is **600 distinct files/content groups**, all assigned to evaluation because the primary threshold is fixed in advance. Actual acquired and accepted counts are currently **0**. There is no TrueSight train split and no threshold-tuning split. Reserve any later technical smoke-test images outside this manifest. Do not describe the 600-image pilot as a full benchmark reproduction.

The two stages target 680 distinct images in total, subject to eligibility and related-content exclusions. Neither stage has acquired samples. The status column above is shorthand only: for **each detector separately**, verify every generator against the exact selected checkpoint's task-training provenance. Record a detector-by-generator matrix with evidence and `seen`, `documented unseen`, or `unresolved`; do not copy a status from one detector to the other. Backbone exposure and image-level overlap are separate checks. Only verified unseen conditions enter that detector's unseen summary; disclose differing condition sets and avoid comparing unlike macro-averages.

Each condition needs 75 eligible real controls, not necessarily one-to-one matched photographs. Confirm their source and content coverage. If archives share real pools, allocate disjoint real groups across conditions using balanced source/content strata; report the resulting allocation and its limitations. If 300 suitable distinct real controls or reliable group identities cannot be obtained, stop and revise the protocol. Do not fill a shortfall by duplicating photographs, invent pairings, or claim 600 unique samples when fewer exist.

## Acquisition and selection, before viewing scores

1. Retain release revision, archive URLs, available upstream checksums, access date, license text, and subset-specific notices. Validate archive integrity after a later authorized download. Inventory original paths, generator versions, labels, real sources, formats, dimensions, and available content/prompt IDs.
2. Detect exact file duplicates with SHA-256 and exact decoded-pixel duplicates. Review near duplicates using a declared perceptual-hash method and cutoff; freeze these settings and the review decisions in the manifest before scoring. Group related crops, renderings, prompts, and source photographs where known. Missing grouping metadata is a documented limitation, not proof of independence.
3. Verify training and validation overlap as described in the feasibility note. Exclude known overlaps from evaluation. Preserve exclusion reasons. If ProGAN independence cannot be established, keep its status explicitly unresolved and withhold H2 interpretation.
4. Exclude corrupt, undecodable, mislabeled, or out-of-scope edited images through score-blind rules. Do not exclude visually convincing images or inconvenient failures. Record every exclusion; if either detector cannot process an image, log the cause and coverage rather than silently deleting it from one model's denominator.
5. Match real and generated samples as closely as the release permits on content category, documented source/collection process, format/codec, resolution, and processing history. Real and synthetic origins cannot be identical; document the intended controls rather than claiming source equivalence. Balance reliable content and resolution strata within conditions and across generators where possible. Keep decoding and any necessary conversion consistent across labels. Preserve originals; do not recompress one label alone or silently normalize away forensic cues. Record matching variables, quotas, and residual differences before selection. Where controls are unavailable, report the mismatch and use stratified descriptive analysis rather than attributing it solely to generator identity. Do not infer categories from detector scores.
6. Select groups deterministically by sorting the SHA-256 digest of the UTF-8 string `TrueSight-R2-v1|<dataset-relative-group-id>` within each frozen stratum, then take the required quota. Break ties by normalized relative path. Allocate shared real pools in the fixed condition order ProGAN, StyleGAN3, GLIDE, FLUX.1-dev without reusing a group. Take one image per group, selected by the same hash ordering of its original relative path. Publish IDs, exclusions, quotas, selection rule, and manifest hash. Any change to this rule requires a dated amendment before scoring.
7. Freeze one manifest per stage, shared by both detectors. Required fields include stage, image ID, release/revision, archive, relative path, file/pixel hash, label, generator/version, per-detector seen-status evidence, real source, content/group IDs, format, dimensions, processing history, evaluation condition, and inclusion/exclusion reason. Use `unknown` for unavailable provenance rather than guessing. Retain source licenses outside image redistribution.

## Detectors and input handling

Use the original official pretrained CNNDetection `weights/blur_jpg_prob0.5.pth` and UniversalFakeDetect `CLIP:ViT-L/14` with `pretrained_weights/fc_weights.pth`. Do not substitute AIGIBench-retrained models. Record downloaded weight SHA-256 values and backbone identity before scoring; weight availability and compatibility are not yet verified.

Source snapshots inspected during planning:

- CNNDetection: `ea0b5622365e3a9cd31d1b54b6b5971131a839ab` ([repository](https://github.com/PeterWang512/CNNDetection/tree/ea0b5622365e3a9cd31d1b54b6b5971131a839ab)).
- UniversalFakeDetect: `030495aea3300a8b54c0ec37ec7fe1dd7e63c619` ([repository](https://github.com/WisconsinAIVision/UniversalFakeDetect/tree/030495aea3300a8b54c0ec37ec7fe1dd7e63c619)).

Use model-native deterministic evaluation preprocessing. For CNNDetection, the planned primary setting is no resizing, a 224-pixel center crop, and ImageNet normalization. For UniversalFakeDetect, inspected `validate.py` uses a 224-pixel center crop without resizing and CLIP normalization. Confirm evaluation flags, padding behavior on small inputs, RGB conversion, interpolation settings where applicable, and package versions against these snapshots before freezing executable commands. No JPEG degradation, random crop, flip, or test-time augmentation is part of this pilot. No-crop CNN inference is a possible later sensitivity analysis, not a silently interchangeable primary setting.

Read source files without recompression. Record handling of orientation and color metadata, and ensure it is deterministic across labels. Neither filename nor metadata is a predictive input. Save original file identity and effective model input dimensions. Native pipelines preserve checkpoint validity, but the comparison covers complete detector pipelines rather than isolating backbone effects.

## Scores, thresholds, and metrics

Define generated = 1 and real = 0. Score semantics and thresholds are detector-specific, not assumed from a shared model interface. Source inspection at the pinned revisions establishes the following for the selected implementations:

| Detector | Native forward output | Official evaluation score and fixed rule |
| --- | --- | --- |
| CNNDetection | Single unbounded affine output from ResNet's final `fc` layer | `validate.py` applies sigmoid and predicts generated when score > 0.5; `demo.py` identifies the synthetic class |
| UniversalFakeDetect, selected CLIP linear head | Single unbounded affine output `fc(encode_image(x))`, not CLIP cosine similarity | `validate.py` assigns real = 0, fake = 1, applies sigmoid, and reports the fixed score > 0.5 rule in addition to an excluded optimized-threshold result |

Evidence: CNNDetection [forward](https://github.com/PeterWang512/CNNDetection/blob/ea0b5622365e3a9cd31d1b54b6b5971131a839ab/networks/resnet.py), [validation](https://github.com/PeterWang512/CNNDetection/blob/ea0b5622365e3a9cd31d1b54b6b5971131a839ab/validate.py), and [demo](https://github.com/PeterWang512/CNNDetection/blob/ea0b5622365e3a9cd31d1b54b6b5971131a839ab/demo.py); UniversalFakeDetect [CLIP head](https://github.com/WisconsinAIVision/UniversalFakeDetect/blob/030495aea3300a8b54c0ec37ec7fe1dd7e63c619/models/clip_models.py) and [validation](https://github.com/WisconsinAIVision/UniversalFakeDetect/blob/030495aea3300a8b54c0ec37ec7fe1dd7e63c619/validate.py).

For these two specific implementations, the independently checked fixed rules happen to coincide: sigmoid score > 0.5. Use each implementation's sigmoid score for the primary confusion counts, with ties assigned real as in its official validation. Save the native scalar separately and use it for AUROC where available to reduce saturation ties; count ranking ties as half a win. A zero native-output threshold is mathematically equivalent but must not replace the documented score rule silently, particularly with finite-precision rounding. These scores are not established calibrated probabilities. Recheck the actual checkpoint, output shape, class mapping, activation, and wrapper in the technical trial before freezing executable evaluation. If any differ, stop and amend the per-detector rule before main scoring. Never flip scores or choose thresholds to improve observed performance.

- **AUROC:** probability that a randomly selected generated image scores above a randomly selected real control, with half credit for ties. Compute separately in each condition; undefined if a class is absent.
- **False-positive rate:** FP / (FP + TN), the fraction of real photographs predicted generated.
- **False-negative rate:** FN / (FN + TP), the fraction of generated images predicted real.
- Report TP, FP, TN, FN, class counts, and processing failures alongside rates for the main experiment only. Show the four conditions individually. For each detector, summarize only its verified unseen conditions with an unweighted macro-average, separate from ProGAN and unresolved conditions. Label this as an average over selected conditions, not the unseen-generator population.

The inspected UniversalFakeDetect entry point calls a test-label-based best-threshold search. **Do not use that optimized threshold or its accuracy as a pilot result.** Its fixed-0.5 outputs and raw scores are usable only after adapting the future evaluation wrapper. No such wrapper is implemented in this task. Any later calibrated threshold requires a new protocol and disjoint validation data, not retrospective tuning of these 600 samples.

For error-rate intervals, report 95% Wilson intervals when image groups are independent. For AUROC and paired detector differences, use 2,000 bootstrap replicates with seed 20261021 at the independent content/source-group level, keeping related images together. Preserve class strata for unrelated groups; for paired real/generated groups resample pairs together. Record the actual grouping scheme and any replicates lacking a class. Reuse resamples across models. With unresolved relatedness, intervals are exploratory. Do not infer independent evidence from repeated real pools.

With only 75 images per class per condition, one mistake changes an error rate by about 1.33 percentage points. Even zero errors leaves a Wilson 95% upper bound near 4.9%. This pilot cannot establish a stable 1% false-positive operating point or small differences between detectors. Avoid significance claims based on the ranking of point estimates.

## Limits and reporting

Generator, real-source, content, codec, and resolution shifts may co-occur. Tabulate these properties by condition and label. CLIP-based curation can favor or alter a CLIP detector's evaluation distribution. Documented absence from task training does not exclude pretraining exposure, generator training-data memorization, or historic benchmark selection effects. Do not claim a causal explanation for failure from these comparisons alone.

Retain commands, environment, hardware, seeds, manifest and weight hashes, per-image scores, coverage failures, and metric calculations. Publish an English report with limitations and actual human/AI contributions. Do not put images, weights, private notes, credentials, or unsupported performance claims into Git. No student contribution beyond what is explicitly evidenced is asserted here.

## Decisions before execution

The researcher approved the research plan in principle with the 80-image technical trial and retained 600-image exploratory main experiment. First establish a lawful, reproducible small-sample acquisition route; the full archive collection must not be downloaded now. Unresolved matching and ProGAN split provenance remain execution gates. If clean H2 evidence is essential, resolve provenance or add a separately documented held-out reference before scoring. Any generator substitution, revised count, new threshold, or sensitivity analysis requires a dated protocol amendment. This documentation task does not run either stage.
