# Reliability under distribution shift: evaluation preparation

Decision recorded: 2026-10-21. Status: evaluation software and synthetic verification only; no real detector experiment, image acquisition, or algorithmic contribution.

## Current objective and scope

The user and ChatGPT selected **Improving the Reliability of AI-Generated Image Detection under Distribution Shift**.

**RQ2: Can existing AI-image detectors identify unreliable predictions when encountering unseen generators?**

R1's cross-generator detection question remains a supporting question. RQ2 asks whether a confidence/acceptance rule can rank a fixed detector's errors and reduce risk at useful coverage on a documented unseen generator. A large authenticity score is evidence toward the generated class, not necessarily confidence in prediction correctness. A score change or detector disagreement alone does not establish unreliability.

Begin with the selected CNNDetection and UniversalFakeDetect checkpoints and fully generated still images versus real photographs. No final reliability algorithm has been chosen. Do not assume checkpoint task-training absence establishes absence from backbone pretraining. Real-source and processing shifts must be tracked alongside generator shifts. The [frontier review](frontier-methods-and-research-gaps.md) provides prior art, including selective classification; adding abstention is not itself a new contribution.

Provisional expectations, not findings:

- **RH1:** Native classifier confidence can rank incorrect predictions poorly under shift. Compare it with random rejection and report negative results.
- **RH2:** A prespecified alternative confidence signal may improve error ranking at matched coverage. Any learned signal must be developed without final-test labels or scores.
- **RH3:** Aggregate gains can hide rejection of one class or one real-image source. Report class/source/generator-specific coverage and risk.

## What R2 already supports, and what it does not

The [R2 protocol](protocol-r2.md) retains its historical status and allocation. Its 80-image technical trial remains pipeline-only. Its 600-image allocation remains an unexecuted exploratory detection plan; it is not automatically a development, validation, and final-test corpus.

| Existing strength | Reliability addition needed |
| --- | --- |
| Per-generator AUROC, FPR/FNR and explicit detector thresholds | Separate authenticity score from confidence; add acceptance rule and selective metrics |
| Source, content, format, resolution and duplicate checks | Group all related samples across every partition, including different transformations and detector outputs |
| Original-checkpoint training provenance | Track exposure of generators to confidence-rule development and validation too |
| Shared manifest for detector comparison | Attach split, confidence-rule identity, implementation/configuration hashes, and processing-failure accounting |
| No test-based threshold tuning | Reserve disjoint development and validation data; freeze acceptance thresholds before final scoring |

No new sample counts are claimed or silently allocated. A later acquisition plan must identify enough independent sources/groups for these partitions. If R2's 600 samples are used to explore reliability methods, mark them `development` and acquire a genuinely independent final test; never relabel explored samples as untouched final evidence. Alternatively, reserve all 600 for evaluation and obtain separate development/validation data before fitting anything. This choice must precede inspecting real detector outputs. Four source groups and 75 samples/class/source cannot establish universal reliability or precise low-FPR guarantees.

## Evaluation definitions and acceptance criteria

Use real = 0 and generated = 1. Preserve the selected detector's score direction, activation, threshold, and tie convention. The current software supports the R2 strict rule `detection_score > decision_threshold`; an incompatible future detector needs an explicit amendment, not an unreported sign flip. Confidence is a separate finite scalar, higher meaning more trusted. It need not be a probability. A native-probability heuristic such as `max(p, 1-p)` is only a baseline once p's meaning is verified.

- **Detection AUROC:** rank generated scores against real scores; half credit for ties. This measures class discrimination, not confidence in correctness.
- **FPR:** FP / number of real scored images. **FNR:** FN / number of generated scored images. Always report counts and full-coverage risk.
- **Risk-coverage:** for acceptance `confidence >= t`, coverage is the accepted fraction of scored samples; risk is the error fraction among accepted samples. Report accepted and rejected counts, rejected-set error rate, class-specific coverage, and accepted-set FPR/FNR. Rejection does not mean real, fake, or correct.
- **AURC v1:** mean prefix risk, `sum(error_count_in_top_k / k for k=1..n) / n`, where confidence sorts descending. Lower is better for a fixed classifier and sample mixture. Within a confidence tie, the module analytically averages over all random orders. The RC output includes only complete tie groups, which are attainable threshold decisions. Therefore its endpoint curve must not be integrated with an unspecified trapezoidal convention to reproduce AURC. AURC is over all scored rows, independently of a chosen operating threshold.

At zero acceptance, risk/FPR/FNR are undefined (`null`), not zero. Single-class AUROC and missing-class rates are `null`. A confidence-tied set has expected AURC equal to its full risk, preventing row order from manufacturing a confidence advantage. Do not transfer a confidence threshold across score scales without verification.

For a future scientific comparison, preregister target coverages (suggested descriptive levels: 50%, 80%, 90%, 100%), acceptance-threshold selection on validation only, class-specific reporting, and random/native-confidence controls. A test-set risk-coverage curve is descriptive, not permission to choose a deployment threshold from test errors. Report actual coverage when ties prevent a target. Compare AURC for confidence rules on the same fixed predictions; across different detectors, different base error rates also change AURC. An improvement claim needs uncertainty estimates, a useful retained fraction, and no concealed class/source failure. No minimum improvement or deployable risk bound has been established.

R2's paired content-group bootstrap remains a future analysis requirement for real results. The current module supplies point estimates, not confidence intervals, calibration fitting, ECE/Brier scores, conformal guarantees, threshold optimization, or automatic leakage detection. Confidence calibration is distinct from selective error ranking. A future probability-calibration study requires verified probabilities, independent fitting data and a separate protocol.

## Partition isolation rules

1. **Synthetic software tests:** manually constructed scores only, marked `simulated`/`synthetic_test`; never counted as images or detector evidence.
2. **Technical trial:** 80 planned images, excluded together with related content groups from subsequent partitions. Use only to validate labels, scores, preprocessing and files. Do not fit confidence rules or quote performance conclusions from it.
3. **Development:** choose features, transformations, confidence-rule architecture, hyperparameters and diagnostics here. Record every generator/source exposed during this process.
4. **Validation:** disjoint content groups; select final configurations, calibrators and operating thresholds here. Once a candidate is selected, freeze it and record the source exposure. Repeated optimization on validation must be disclosed.
5. **Final test:** unopened for method selection. Freeze protocol, manifests, weight/configuration hashes, confidence rule and thresholds before scoring. Do not use even unlabeled final scores to select features, normalization, clusters, mixtures, or acceptance settings. Test labels may be used only by the final evaluator. The module computes errors, so it should be run by a final-evaluation process after the rule is fixed; it is not a security boundary.

For a strict unseen-generator reliability claim, reserve a generator absent from detector task training **and** from development/validation of the confidence rule. Document both statuses for each detector. Also retain a source-shift check for real photographs; unfamiliar real images are not automatically generated. Related prompt/source-photo/crop/codec variants and duplicates must stay in one partition across all datasets and model runs. Audit byte/pixel hashes and available group IDs across partitions; unresolved grouping is a limitation. Do not create a split by shuffling rows after scoring. Keep the same final sample set for paired rule comparisons.

Any post-test revision consumes that test set as development evidence; obtain a new final test for confirmatory claims. Record failed methods and test exposure in the log. Do not tune the acceptance threshold on the 80-image trial or on the 600-image test while calling it validation-free.

## Input and output contract for future GPU runs

The reusable evaluator lives in [the evaluation module](../truesight/reliability.py); its [CSV interface](../truesight/evaluate.py) does not load models or fit a rule. Python 3.11's standard library is sufficient. Run from the repository root:

```text
py -3.11 -m unittest discover -s tests -v
py -3.11 -m truesight.evaluate INPUT.csv NEW_OUTPUT.json --decision-threshold THRESHOLD --acceptance-threshold ACCEPT_AT
```

Omit `--acceptance-threshold` to accept every successfully scored row. Output paths must be new; existing files are not overwritten. No package installation is required. [The fixture](../tests/fixtures/simulated_predictions.csv) contains invented scores and explicitly labeled simulated failures.

Minimum CSV columns enforced by the interface:

| Field | Meaning |
| --- | --- |
| `sample_id` | Nonempty, unique within one detector/run file |
| `label` | `0` real, `1` generated; required even for failed rows for class-level accounting |
| `detection_score` | Finite score in a documented generated-positive direction, separate from confidence |
| `confidence_score` | Finite acceptance-ranking score; required on successful rows |
| `status`, `error_reason` | `ok` or `error`; failed rows require a reason and may omit scores |
| `data_kind` | `simulated` or `real_detector_output`, never mixed |
| `split` | `synthetic_test`, `technical_trial`, `development`, `validation`, or `final_test`; only simulations use `synthetic_test` |
| `evaluation_condition` | Prespecified source/generator condition; real controls assigned to their comparison condition |

One file must contain one split, one data kind and one detector/checkpoint/confidence-rule run. The latter run identity is a caller responsibility, recorded in its sidecar. Real-data eligibility requires the full manifest/sidecar below; the small CSV reader does not certify it. AUROC and RC may use different documented score transformations only if their orientation and threshold semantics are consistent; keep native outputs for audit.

Before a real experiment, require a joined manifest with `group_id`, dataset/revision, relative source ID, file/pixel hashes, generator/version, real source, content class, codec, dimensions, processing history, split, and separate per-detector/per-confidence-rule exposure statuses. Require a run sidecar with protocol version, code revision, manifest hash, detector/checkpoint/backbone identifiers and hashes, native score definition/activation, confidence-rule ID/configuration and fitting-data manifest hashes, threshold values and their selection provenance, preprocessing, seed, precision, hardware, dependency versions and failure policy. Store native scores and predicted labels in the GPU export for cross-checking; the evaluator recomputes predictions from the declared rule. Absolute private paths or credentials do not belong in public manifests.

The JSON output carries a schema version, simulation marker, split, thresholds, overall and per-condition metrics, confusion counts and RC points. Failed rows remain in `input_count`, `failure_count`, class-specific failure counts, scoring coverage and end-to-end acceptance coverage. Detection/selective risks use only successfully scored rows and must be labeled accordingly; do not interpret a low risk with low scoring coverage as safe operation. All-failed conditions produce `null` metrics. The pooled summary is descriptive; it is not a verified unseen-condition macro-average. Seen/unseen filtering and scientific summaries require the provenance audit.

Retain the original CSV, sidecar, manifest, JSON and software-test log under immutable run identifiers outside private notes. A later GPU worker need only export this contract; a model plugin system is unnecessary. Do not commit weights, datasets or large caches. Public reports and comments remain English; Chinese discussion notes remain outside the public repository.
