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
