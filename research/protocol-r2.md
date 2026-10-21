# R2 draft protocol: Cross-generator detector evaluation

Version: 0.1, 2026-10-21. Status: **draft; no runs or results**. This document registers a proposed pilot, not an executed experiment. The user selected CNNDetection and UniversalFakeDetect as the Phase 1 baselines. Data selection is recommended by Codex and remains conditional on the [feasibility checks](data-feasibility-r2.md).

## Question and intended inference

[RQ1](questions.md): How well do existing AI-generated image detectors generalize to unseen image generators?

Estimate each fixed detector's discrimination and error rates on specified public subsets. Test H1 descriptively across conditions. Assess H2 only if a genuinely held-out seen-generator reference can be established. H3 is a limitation to investigate, not a causal conclusion this pilot can settle. One GAN and two diffusion-family unseen candidates do not support a population-level claim about all generators or an architecture-only comparison.

## Conditions and sample accounting

Use AIGIBench's public **test** archives at the revision recorded in the feasibility note. No task training, fine-tuning, calibration fitting, or synthetic image collection is planned.

| Condition | Generator status relative to the selected original checkpoints | Real | Generated |
| --- | --- | ---: | ---: |
| ProGAN | Seen generator; sample independence pending | 75 | 75 |
| StyleGAN3 | Candidate unseen GAN | 75 | 75 |
| GLIDE | Candidate unseen older diffusion model | 75 | 75 |
| FLUX.1-dev | Candidate unseen relatively newer diffusion-family model | 75 | 75 |
| Target | Four conditions | 300 | 300 |

The target is **600 distinct files/content groups**, all assigned to evaluation because the primary threshold is fixed in advance. Actual acquired and accepted counts are currently **0**. There is no TrueSight train split and no threshold-tuning split. Reserve any later technical smoke-test images outside this manifest. Do not describe the 600-image pilot as a full benchmark reproduction.

Each condition needs 75 eligible real controls, not necessarily one-to-one matched photographs. Confirm their source and content coverage. If archives share real pools, allocate disjoint real groups across conditions using balanced source/content strata; report the resulting allocation and its limitations. If 300 suitable distinct real controls or reliable group identities cannot be obtained, stop and revise the protocol. Do not fill a shortfall by duplicating photographs, invent pairings, or claim 600 unique samples when fewer exist.

## Acquisition and selection, before viewing scores

1. Retain release revision, archive URLs, available upstream checksums, access date, license text, and subset-specific notices. Validate archive integrity after a later authorized download. Inventory original paths, generator versions, labels, real sources, formats, dimensions, and available content/prompt IDs.
2. Detect exact file duplicates with SHA-256 and exact decoded-pixel duplicates. Review near duplicates using a declared perceptual-hash method and cutoff; freeze these settings and the review decisions in the manifest before scoring. Group related crops, renderings, prompts, and source photographs where known. Missing grouping metadata is a documented limitation, not proof of independence.
3. Verify training and validation overlap as described in the feasibility note. Exclude known overlaps from evaluation. Preserve exclusion reasons. If ProGAN independence cannot be established, keep its status explicitly unresolved and withhold H2 interpretation.
4. Exclude corrupt, undecodable, mislabeled, or out-of-scope edited images through score-blind rules. Do not exclude visually convincing images or inconvenient failures. Record every exclusion; if either detector cannot process an image, log the cause and coverage rather than silently deleting it from one model's denominator.
5. Balance real and generated content strata within a condition where reliable annotations exist. Use common content strata across conditions only where supported by metadata. Do not infer category labels from detector scores. Record exact stratum quotas before selection; if categories cannot be matched, retain source-stratified descriptive comparisons and explicitly state that content matching was unavailable.
6. Select groups deterministically by sorting the SHA-256 digest of the UTF-8 string `TrueSight-R2-v1|<dataset-relative-group-id>` within each frozen stratum, then take the required quota. Break ties by normalized relative path. Allocate shared real pools in the fixed condition order ProGAN, StyleGAN3, GLIDE, FLUX.1-dev without reusing a group. Take one image per group, selected by the same hash ordering of its original relative path. Publish IDs, exclusions, quotas, selection rule, and manifest hash. Any change to this rule requires a dated amendment before scoring.
7. Freeze one manifest used by both detectors. Required fields include image ID, release/revision, archive, relative path, file/pixel hash, label, generator/version, seen-status evidence, real source, content/group IDs, format, dimensions, evaluation condition, and inclusion/exclusion reason. Use `unknown` for unavailable provenance rather than guessing. Retain source licenses outside image redistribution.

## Detectors and input handling

Use the original official pretrained CNNDetection `weights/blur_jpg_prob0.5.pth` and UniversalFakeDetect `CLIP:ViT-L/14` with `pretrained_weights/fc_weights.pth`. Do not substitute AIGIBench-retrained models. Record downloaded weight SHA-256 values and backbone identity before scoring; weight availability and compatibility are not yet verified.

Source snapshots inspected during planning:

- CNNDetection: `ea0b5622365e3a9cd31d1b54b6b5971131a839ab` ([repository](https://github.com/PeterWang512/CNNDetection/tree/ea0b5622365e3a9cd31d1b54b6b5971131a839ab)).
- UniversalFakeDetect: `030495aea3300a8b54c0ec37ec7fe1dd7e63c619` ([repository](https://github.com/WisconsinAIVision/UniversalFakeDetect/tree/030495aea3300a8b54c0ec37ec7fe1dd7e63c619)).

Use model-native deterministic evaluation preprocessing. For CNNDetection, the planned primary setting is no resizing, a 224-pixel center crop, and ImageNet normalization. For UniversalFakeDetect, inspected `validate.py` uses a 224-pixel center crop without resizing and CLIP normalization. Confirm evaluation flags, padding behavior on small inputs, RGB conversion, interpolation settings where applicable, and package versions against these snapshots before freezing executable commands. No JPEG degradation, random crop, flip, or test-time augmentation is part of this pilot. No-crop CNN inference is a possible later sensitivity analysis, not a silently interchangeable primary setting.

Read source files without recompression. Record handling of orientation and color metadata, and ensure it is deterministic across labels. Neither filename nor metadata is a predictive input. Save original file identity and effective model input dimensions. Native pipelines preserve checkpoint validity, but the comparison covers complete detector pipelines rather than isolating backbone effects.

## Scores, thresholds, and metrics

Define generated = 1 and real = 0. Higher scores must mean more evidence for generated images. Save logits and sigmoid scores when available. Use the logit for AUROC to avoid saturation ties when possible; count tied scores as half a win. Verify score direction from code and separate smoke tests, never by flipping scores to improve evaluation AUROC.

Primary decision rule: **generated if logit > 0**, equivalently sigmoid score > 0.5 in exact arithmetic; otherwise real. Use the logit rule to resolve finite-precision sigmoid rounding, and retain both scores. This is a fixed operating threshold, not a calibrated probability claim. Report it for both models without tuning it per generator.

- **AUROC:** probability that a randomly selected generated image scores above a randomly selected real control, with half credit for ties. Compute separately in each condition; undefined if a class is absent.
- **False-positive rate:** FP / (FP + TN), the fraction of real photographs predicted generated.
- **False-negative rate:** FN / (FN + TP), the fraction of generated images predicted real.
- Report TP, FP, TN, FN, class counts, and processing failures alongside rates. Show the four conditions individually. Summarize the three candidate unseen conditions with an unweighted macro-average, separate from ProGAN. Label this as an average over selected conditions, not the unseen-generator population.

The inspected UniversalFakeDetect entry point calls a test-label-based best-threshold search. **Do not use that optimized threshold or its accuracy as a pilot result.** Its fixed-0.5 outputs and raw scores are usable only after adapting the future evaluation wrapper. No such wrapper is implemented in this task. Any later calibrated threshold requires a new protocol and disjoint validation data, not retrospective tuning of these 600 samples.

For error-rate intervals, report 95% Wilson intervals when image groups are independent. For AUROC and paired detector differences, use 2,000 bootstrap replicates with seed 20261021 at the independent content/source-group level, keeping related images together. Preserve class strata for unrelated groups; for paired real/generated groups resample pairs together. Record the actual grouping scheme and any replicates lacking a class. Reuse resamples across models. With unresolved relatedness, intervals are exploratory. Do not infer independent evidence from repeated real pools.

With only 75 images per class per condition, one mistake changes an error rate by about 1.33 percentage points. Even zero errors leaves a Wilson 95% upper bound near 4.9%. This pilot cannot establish a stable 1% false-positive operating point or small differences between detectors. Avoid significance claims based on the ranking of point estimates.

## Limits and reporting

Generator, real-source, content, codec, and resolution shifts may co-occur. Tabulate these properties by condition and label. CLIP-based curation can favor or alter a CLIP detector's evaluation distribution. Documented absence from task training does not exclude pretraining exposure, generator training-data memorization, or historic benchmark selection effects. Do not claim a causal explanation for failure from these comparisons alone.

Retain commands, environment, hardware, seeds, manifest and weight hashes, per-image scores, coverage failures, and metric calculations. Publish an English report with limitations and actual human/AI contributions. Do not put images, weights, private notes, credentials, or unsupported performance claims into Git. No student contribution beyond what is explicitly evidenced is asserted here.

## Decisions before execution

Recommended default: accept the four-condition allocation and fixed-threshold exploratory scope, subject to provenance checks. The researcher still needs to accept the archive/storage cost and decide whether unresolved real-source matching or ProGAN split provenance is acceptable for descriptive reporting. If clean H2 evidence is essential, resolve provenance or add a separately documented held-out reference before scoring. Any generator substitution, revised count, new threshold, or sensitivity analysis requires a dated protocol amendment.
