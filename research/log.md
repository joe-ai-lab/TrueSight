# Research log

## 2026-10-21 — Research restart (M0)

### Starting state

The repository was cloned from GitHub. The local history inspected for this restart contains three commits:

| Commit | Date | Change |
| --- | --- | --- |
| `9381496` | 2025-07-28 | Created the project README |
| `51567cd` | 2025-07-31 | Added the notebook directory placeholder |
| `ea1cf64` | 2025-07-31 | Added the image-loading and display notebook |

At that starting revision, the tracked files were `README.md`, `notebook/.gitkeep`, and `notebook/TrueSight_Demo.ipynb`. The notebook imports Pillow and Matplotlib, opens `demo.jpg`, displays it, and prints that prediction is not implemented. It contains saved output from a previous execution, but the referenced image is absent from the repository. That output does not establish that the current checkout can reproduce the execution.

No detector implementation, model weights, dataset manifest, dependency specification, evaluation protocol, or experiment results were present. The original README's references to model training, Grad-CAM, and a possible web demo were aspirations, not completed work.

### Decision and rationale

The user and ChatGPT selected **Generalization and Reliability of AI-Generated Image Detection** as the research direction. The first question is [RQ1](questions.md): **How well do existing AI-generated image detectors generalize to unseen image generators?**

This shifts the immediate priority from building a detection demo or training a new model to evaluating existing methods. A prediction on a few images cannot establish generalization. A controlled comparison can instead support research practice in dataset inspection, evaluation, uncertainty, and error analysis. It also creates a basis for later reliability studies without assuming that an algorithmic contribution is already needed.

The longer-term aims are to help an undergraduate explore suitable AI research directions before choosing a focus in 2027 and to build authentic, reproducible work for future overseas master's applications. These are motivations, not claims of research achievement.

### Current expectations and next investigation

[H1–H3](questions.md#provisional-hypotheses) concern variation across generators, a possible seen-to-unseen performance gap, and confounding from image properties or sources. None has been tested in TrueSight.

Next, investigate the official CNNDetection and UniversalFakeDetect baselines and suitable evaluation data. Check access, licenses, training overlap, preprocessing, and computing requirements before finalizing an experiment protocol. Candidate selection remains provisional.

### Work completed and limits

This maintenance task establishes Markdown entry points for research questions, decisions, and future experiments. Codex prepared these records from the repository and the user's stated research decisions. No student implementation, analysis, or experimental contribution is asserted.

No models were installed, no datasets were downloaded, and no detector inference, training, or evaluation was performed during this restart. There are no detector results to report. The original README, notebook, and prior Git history are preserved.

## 2026-10-21 — Phase 1 / R2: Data feasibility and draft protocol

The user selected CNNDetection and UniversalFakeDetect, public data with documented sources, an initial sample near 600 images, and AUROC, false-positive rate, and false-negative rate with per-generator reporting. This task investigated sources and wrote a protocol; it did not execute that protocol.

Codex inspected official repository documentation, relevant preprocessing and threshold code, dataset cards, license files, and public metadata endpoints. The [feasibility note](data-feasibility-r2.md) recommends selected AIGIBench test archives and records Synthbuster/RAISE and GenImage as alternatives with different coverage and access limitations. AIGIBench's metadata and archive sizes were accessible; no full data transfer or image-level provenance verification was performed.

The [protocol draft](protocol-r2.md) proposes 75 real and 75 generated images for each of ProGAN, StyleGAN3, GLIDE, and FLUX.1-dev. ProGAN is a seen-generator reference, not an unseen condition. The target is 600 distinct eligible samples; acquired and accepted counts remain zero. Actual counts and a manifest can only be established after later acquisition and duplicate/source checks.

The recommended primary threshold is fixed at logit zero, with no test-based tuning. Source inspection found that UniversalFakeDetect's validation entry point also computes a best threshold from test labels; that path must not supply the pilot's operating threshold. The planned original checkpoints must not be confused with AIGIBench's retrained checkpoints.

Open issues are real-source/content matching, independence of the ProGAN test samples, unverifiable backbone exposure, archive storage cost, and researcher acceptance of the exploratory sample size. These are explicit limits rather than resolved findings. Earlier hypotheses remain untested. The draft does not freeze a dataset manifest or claim results, complete reproducibility, or student experimental contributions.

No packages, models, or datasets were installed or downloaded. No inference, training, or formal evaluation was run. Public changes are English Markdown only. Publication to GitHub requires user confirmation after review of the local commit.

## 2026-10-21 — R2 revision 0.2: Technical trial and selective access

The user approved R2 in principle and authorized publication of the research documents with this revision. The [protocol](protocol-r2.md) now separates an 80-image technical trial (10 real and 10 generated per source) from the retained 600-image exploratory main experiment. Trial outputs cannot support performance conclusions; trial images and related content groups must be excluded from the main sample. Both stages remain unexecuted with zero acquired images.

Seen/unseen provenance must be checked independently for every detector-generator combination. Matching requirements now explicitly cover content, sources, format, resolution, and processing history. Pinned source inspection confirms that CNNDetection returns a scalar affine ResNet output, while the selected UniversalFakeDetect head returns a scalar affine output on CLIP features. Each official validator separately applies sigmoid and a fixed > 0.5 rule. The revised primary rule follows those validators, replacing version 0.1's universal native-output threshold assumption. Actual checkpoint/wrapper semantics still require later technical validation; test-label-based threshold optimization remains excluded.

The user deferred the 19.46 GB archive collection. The [access investigation](data-feasibility-r2.md#small-sample-access-investigation) prioritizes traceable official small releases and selective ZIP access. A ProGAN HEAD-only request advertised byte-range support; no archive payload or image was fetched, and selective extraction remains untested. No model was run, no large dataset was downloaded, and no results or student experimental contributions are claimed. Earlier entries retain the decision history; version 0.2 supersedes their threshold and acquisition recommendations.
