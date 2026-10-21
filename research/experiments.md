# Experiment record

**No research experiments have been run.** The existing notebook is an image-display demonstration with a placeholder prediction message, not a detector experiment.

Update, 2026-10-21: [reliability preparation](reliability-protocol.md) adds a reusable score evaluator and partition rules for the current RQ2. [Software verification](validation/reliability-validation.md) records 15 passing unit tests and a successful simulated CSV run. These are software checks with invented scores, not research experiments or image detector results. R2's real technical trial and main experiment remain unexecuted.

R2 now has a [protocol draft, version 0.2](protocol-r2.md) and [data feasibility review](data-feasibility-r2.md) for [RQ1](questions.md). The research plan is approved in principle; small-sample access and image-level provenance checks remain pending. Stage A is an 80-image technical trial (four sources, each with 10 real and 10 generated images) for pipeline validation only. Stage B retains the 600-image exploratory main experiment, excluding trial images and related groups. Acquired images in both stages: 0. Neither stage has run; no performance numbers or conclusions are available. The 19.46 GB full archive collection is deferred.

## When experiments begin

Add a dated entry here with a stable experiment identifier and a link to its record. Before a run, record the question or hypothesis, data sources and split manifest, detector and weight versions, preprocessing, metrics, threshold-selection rule, and planned comparisons.

For each executed run, retain the code revision, exact command and configuration, environment and hardware, random seeds where applicable, artifact checksums, logs, and per-image scores. Summaries must link to their underlying outputs and state limitations. Distinguish planned, running, completed, and failed work; a completed run may still be scientifically inconclusive.

Record failed runs and unexpected findings with their impact on earlier conclusions. If a configuration, metric, or dataset is corrected, preserve the earlier record and identify which results have been superseded. Record actual human and AI contributions alongside the work, without inventing participation.
