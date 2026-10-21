# Reliability module verification: simulated data only

Recorded: 2026-10-21. **This is a software test record, not an AI-image detection experiment.** No photographs, generated images, detector checkpoints, or GPU were used. The fixture's labels, scores and failures were manually invented.

## Executed checks

Python 3.11.6, standard library only. The [captured test log](reliability-synthetic-tests.txt) contains the actual timestamp, source SHA-256 hashes, commands, outputs and exit codes. All **15 unittest tests passed**; the fixture CSV evaluation command also exited successfully. No dependencies were installed.

Coverage includes perfect predictions, high-confidence errors, imbalanced labels, full and zero acceptance, missing classes, boundary equality, tied scores, invalid/nonfinite inputs, duplicate IDs, mixed partitions, explicit simulation markers, failed processing, condition-level reporting, command-line evaluation and output-overwrite protection.

For AUROC, the rank implementation was compared with an independent pairwise oracle over all 243 score assignments of a five-label fixture. For tied-confidence AURC, the analytic expectation was compared with exhaustive within-tie permutations. These checks validate arithmetic and conventions, not robustness to actual image-domain shifts.

## Fixture outputs

[Saved JSON](simulated-reliability-results.json) was produced from [the simulated CSV](../../tests/fixtures/simulated_predictions.csv) with detection threshold 0.5 and acceptance threshold 0.95. It contains 12 invented rows: 11 scored and one deliberately failed. The pooled result is only a software diagnostic.

| Invented condition | Scored rows | AUROC | AURC | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Normal predictions | 2 | 1.0 | 0.0 | Arithmetic sanity check |
| High-confidence errors | 4 | 0.25 | 0.7916666667 | Confidence ranks both wrong predictions first |
| Imbalanced labels | 5 | 0.125 | 0.13 | Detection discrimination and error ranking measure different properties |
| Pipeline failure | 0 | undefined | undefined | Failure counted; no fabricated scores or metrics |

In the high-confidence-error fixture, full risk is 0.5, while accepting scores >= 0.95 retains half the rows with risk 1.0. Thus selective prediction can worsen risk when confidence is misleading. These values were designed to exercise that failure mode; they are not measured properties of CNNDetection, UniversalFakeDetect, or any image dataset.

## Remaining limits

The software has not been exercised on real detector exports. It does not estimate scientific confidence intervals, fit confidence rules, audit training overlap, enforce cross-file split isolation, or certify probabilities. Real-source shifts, unseen-generator status and low-FPR behavior remain untested. The current point-estimate module is evaluation infrastructure, not a detection or reliability algorithm.
