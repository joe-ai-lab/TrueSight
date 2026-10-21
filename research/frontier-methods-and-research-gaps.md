# Frontier Methods and Research Gaps

Review date and cutoff: **2026-10-21**. This review covers material available by that date, not the remainder of October. It is a focused investigation, not an exhaustive survey. TrueSight has defined R1 and the R2 protocol; **no detector inference, training, or formal experiment has been performed**. No final algorithm is selected here.

## 1. Evidence standards and source verification

**Verified record** means a publication, source file, or resource listing was inspected. **Author-reported evidence** means a result appears in a paper; it has not been independently reproduced by TrueSight. **Our analysis/hypothesis** means an interpretation or proposed test, not an established result. Publication does not turn a universal claim into a universal guarantee. A weight link is not a verified download or successful reproduction.

| Method | Identity and publication record | Official implementation and reproducibility status |
| --- | --- | --- |
| RA-Det, Wang et al. | [ICML 2026, PMLR 306:125515-125532](https://proceedings.mlr.press/v306/wang26ad.html); [arXiv v1](https://arxiv.org/html/2603.01544v1) | [Author-linked repository](https://github.com/dongdongunique/RA-Det), snapshot `591d4c0d24798b49dc881af58093883c6fdf45f9`. Code exists; no trained detector/prober weight download was located in the inspected README, release note, tree, or GitHub releases. DINOv3 backbone weights alone are insufficient. No root license was identified in that inspection; resolve permissions before reuse. |
| DID, Qi et al. | [CVPR 2026, pp. 42964-42975](https://openaccess.thecvf.com/content/CVPR2026/html/Qi_A_Difference-in-Difference_Approach_to_Detecting_AI-Generated_Images_CVPR_2026_paper.html); [arXiv v1](https://arxiv.org/html/2602.23732v1) | [Official repository](https://github.com/Qixinyi1122-lucky/DID), snapshot `317b36fc99b5d6b2c22f1854a393b9a757c8bdc7`, MIT. Reconstruction, detector training/testing, and fusion code exist. No downloadable trained pair of detector checkpoints was located in the inspected README/tree/releases. This is a negative search result, not proof that none exists elsewhere. |
| DoU, He et al. | [CVPR 2026, pp. 40407-40417](https://openaccess.thecvf.com/content/CVPR2026/html/He_Diversity_over_Uniformity_Rethinking_Representation_in_Generated_Image_Detection_CVPR_2026_paper.html); [arXiv v1](https://arxiv.org/html/2603.00717v1) | [Official repository](https://github.com/Yanmou-Hui/DoU), snapshot `230856fabd137e00580d5457b3b1ce7b664bcf99`, MIT. Evaluation code and Google Drive/Baidu checkpoint links are provided; training code/configuration are explicitly pending. Inference is a candidate; full training reproduction is incomplete. |
| WaRPAD, Choi et al. | [NeurIPS 2025 proceedings paper](https://papers.neurips.cc/paper_files/paper/2025/file/1d8f05e4da49a4e1e1b052a3046bceac-Paper-Conference.pdf); [arXiv](https://arxiv.org/html/2511.14030v1) | [Author repository](https://github.com/sungikchoi/WaRPAD), snapshot `59f2b382171e579f2b7e180165b327f10332152b`. Evaluation code exists, with pretrained backbone rather than a learned detector checkpoint. No repository license was identified in the inspected listing. |
| B-Free, Guillaro et al. | [CVPR 2025, pp. 18685-18694](https://openaccess.thecvf.com/content/CVPR2025/html/Guillaro_A_Bias-Free_Training_Paradigm_for_More_General_AI-generated_Image_Detection_CVPR_2025_paper.html) | [Official repository](https://github.com/grip-unina/B-Free), snapshot `c6a9f898782fb466b29af01f21960b67415afb0e`. Inference instructions, weight URL and archive MD5 exist; informational/nonprofit software terms apply. |
| WePe, Nie et al. | [Epistemic Uncertainty for Generated Image Detection, NeurIPS 2025](https://papers.nips.cc/paper_files/paper/2025/hash/927dfe0d77fb20d9822bacd6737375a8-Abstract-Conference.html) | [Paper-linked repository](https://github.com/tmlr-group/WePe) resolves; source listing includes `wepe.py`, perturbation utilities and MIT license. A complete ready-to-run reproduction guide and trained-variant weights were not established in this review. |
| ReSIDe, Zheng and Seidman | [arXiv:2605.08574v1](https://arxiv.org/html/2605.08574v1), May 2026 | [Author announcement](https://www.linkedin.com/posts/kaixiang-zheng-113665229_post-hoc-selective-classification-for-reliable-activity-7509413690744504320-P3s-) claims NeurIPS 2026 acceptance. An official proceedings/acceptance record and author-linked implementation were not independently established here. Treat the inspected preprint as the technical source; do not call it formally published in NeurIPS proceedings. |

Only paper PDFs/text, source code text and metadata were retrieved for reading. No model weights or dataset images were downloaded; no external code was executed. Repository code licenses do not automatically cover backbone weights, datasets, or generated outputs. All resources require renewed access and license checks before execution.

## 2. Baseline context

The original [CNNDetection](https://github.com/PeterWang512/CNNDetection) learns a ResNet image classifier from ProGAN/LSUN with augmentations. [UniversalFakeDetect](https://github.com/WisconsinAIVision/UniversalFakeDetect) uses a frozen CLIP feature space and a trained linear classifier for the selected checkpoint. Both score the image directly. The methods below change the evidence, the representation-learning objective, or the decision to accept a prediction. None automatically inherits R2's training provenance or threshold rule.

## 3. RA-Det: Learn a probe that exposes robustness differences

**Author-reported mechanism.** A frozen encoder supplies clean and perturbed embeddings. A learned conditional UNet produces a bounded probe, schematically

\[
x'=x+\epsilon\tanh P_\phi(x,f(x)),\qquad e=f(x),\quad e'=f(x').
\]

Semantic, discrepancy and pixel-residual branches contribute classification evidence. Discrepancies include distance, vector differences and similarity. Training combines binary cross-entropy with

\[
L_{RA}=\max(0,\bar s_{fake}-\bar s_{real}+\gamma),\quad s=\cos(e,e').
\]

The [formal paper](https://raw.githubusercontent.com/mlresearch/v306/main/assets/wang26ad/wang26ad.pdf), Sections 3-5/Table 1, reports ProGAN task training, DINOv3 ViT-L/16, and 16 primary evaluation conditions. Mean ACC/AP are 93.47/97.00%, versus FerretNet 85.66/90.43%. Thus the ACC difference is **7.81 percentage points** in that table. The proceedings abstract instead says 12.92% average improvement; the v1 abstract/repository says 7.81%. These are not interchangeable, and the abstract's denominator is not resolved by this review. ACC/AP are not TrueSight AUROC/FPR/FNR results.

**Verified implementation conditions.** The repository recommends batch 256, eight GPUs and a short training example; the formal paper describes ten epochs, batch 32 and eight H200s. Those instructions need reconciliation. The README's “data- and model-agnostic” wording does not mean training-free. A complete reproduction requires the learned prober and heads, not just the frozen encoder.

**Our analysis.** A local expansion gives

\[
\mathbb E_\delta\|f(x+\delta)-f(x)\|^2\approx\operatorname{tr}(J_f(x)\Sigma_\delta J_f(x)^T).
\]

This describes encoder sensitivity, not authenticity by itself. The paper's memorization-linked bound depends on smoothness, manifold/sensitivity assumptions and a sufficiently favorable divergence term; a lower bound need not be positive. Its isotropic small-probe analysis is not automatically a guarantee for a learned structured probe, every photograph, or every future generator. Training a probe to separate known labels can also amplify source/codec shortcuts. To isolate behavior from the richer detector, compare matched-backbone clean-only, fixed-probe and learned-probe variants with equal data and compute. Audit any batch-statistics features for sensitivity to inference batch composition. RA-Det's paper also uses a real/fake label convention opposite to R2 in its contrastive-loss notation: map it explicitly.

## 4. DID: Difference the residuals, not just the images

**Author-reported mechanism.** With a fixed reconstruction operator R,

\[
x'=R(x),\quad x''=R(x'),\quad r_1=|x-x'|,\quad r_2=|x'-x''|,\quad d=r_1-r_2.
\]

The final difference is signed. Separate supervised classifiers consume first- and second-order residual maps. This extends DIRE, rather than being a training-free alternative to it. The [formal paper](https://openaccess.thecvf.com/content/CVPR2026/papers/Qi_A_Difference-in-Difference_Approach_to_Detecting_AI-Generated_Images_CVPR_2026_paper.pdf), Tables 1-2, reports accuracy on LSUN-Bedroom, ImageNet and LAION conditions. With ImageNet/ADM training, DID/DIRE total ACC is 99.41/99.37%; with smaller LAION/Kandinsky-3 and LAION/SDXL training, 94.55/92.96% and 96.42/94.83%. The latter gains are **1.59 points**, not 20-30 accuracy points; relative error reduction is a different quantity. Its supplementary cost analysis reports 2.46 seconds/image on an A800, not a local runtime promise.

**Verified implementation conditions.** The repository uses ADM reconstruction, two ResNet classifiers and configurable fusion. `SUP=True` uses the minimum branch probability (both must vote fake); the alternative uses either branch. The paper's main prose says real only if both vote real, so the example `SUP=True` command is not interchangeable with that rule. Its code default threshold is 0.5, with approximately 0.29 documented for a paper setting. See [fusion code](https://github.com/Qixinyi1122-lucky/DID/blob/317b36fc99b5d6b2c22f1854a393b9a757c8bdc7/fusion/evaluate.py). Resolve branch meaning, fusion, signed-map scaling and checkpoint provenance before reproducing a headline number.

**Our analysis.** Cancellation is conditional, not automatic:

\[
\operatorname{Var}(r_1-r_2)=\operatorname{Var}(r_1)+\operatorname{Var}(r_2)-2\operatorname{Cov}(r_1,r_2).
\]

Positive correlation can help; independent reconstruction noise can increase variance. The manifold approximation also assumes synthetic inputs are close to the reconstruction model's manifold, which is not guaranteed for unseen GANs or flow models. The nominal 0.29 threshold does not generally equalize empirical FPR across dependent, uncalibrated branches. Compare ROC and matched-validation-FPR operating points, not only default-threshold ACC. Reconstruction evidence is derived from the same image: a deterministic transformation cannot create new information about its label, although it can expose information a particular classifier misses. Statistical independence from CLIP/CNN scores must be tested, not asserted. Repeated reconstruction itself is already published prior art.

## 5. DoU: Preserve multiple discriminative representations

**Author-reported mechanism.** The [formal CVPR paper](https://openaccess.thecvf.com/content/CVPR2026/papers/He_Diversity_over_Uniformity_Rethinking_Representation_in_Generated_Image_Detection_CVPR_2026_paper.pdf), Section 4, uses frozen multi-stage CLIP features, variational cue bottlenecks, cue-removal consistency, and anti-collapse learning. For a cue, a representative bottleneck is

\[
z_i=\mu_i(v_i)+\sigma_i(v_i)\odot\eta_i,\quad\eta_i\sim N(0,I).
\]

Pairwise dependence is penalized through empirical HSIC:

\[
\mathrm{HSIC}_{ij}=\operatorname{tr}(K_iHK_jH)/(B-1)^2.
\]

Learned convex cue weights receive a concentration penalty; the aggregate aligns with learned real/fake text prototypes. Unlike UniversalFakeDetect's single linear head, this requires trained bottlenecks, aggregation and prompts. Training uses GenImage SD1.4; evaluation covers UniversalFakeDetect, GenImage and AIGI-Holmes with ACC/AP and class-specific metrics. The inspected [v1 results](https://arxiv.org/html/2603.00717v1), Section 5/Table 1, report mean ACC/AP 92.81/99.52%, cross-generator ACC 90.02%, and baseline 87.81% mean ACC. These are explicitly v1 figures; its abstract's 5.02% improvement differs from the body comparison. Do not merge versions or compare that AP to RA-Det's different test mixture.

**Verified implementation conditions.** The [released code](https://github.com/Yanmou-Hui/DoU/blob/230856fabd137e00580d5457b3b1ce7b664bcf99/models/dou.py) samples latent noise in its forward path without an obvious evaluation-only mean substitution. Its aggregation weights are feature-dimension-dependent, more detailed than a scalar-weight summary. `test.py` supports CPU, but loads checkpoints with `strict=False`; missing/unexpected keys must be audited. Weight links are advertised, not downloaded or hash-verified. Training is not fully reproducible from the current release alone.

**Our analysis.** Higher effective rank does not prove more independent authenticity evidence: nuisance dimensions can increase rank too. Low empirical HSIC on a batch is not proof of causal independence, and shared labels necessarily create some useful dependence. Compare matched-capacity models with independent nuisance controls, not rank alone. A repeated-seed inference audit is essential before attributing score changes to image perturbations. The final CIB formulation differs from the early arXiv derivation; use the formal version and released implementation together, not an unverified generic mutual-information identity. SD1.4 is seen for this model even though it is unseen for the original ProGAN-trained TrueSight baselines; status is checkpoint-specific.

## 6. Other representative work that constrains novelty

### WaRPAD (NeurIPS 2025): A feasible response-based comparator

**Author-reported:** With Haar high-frequency content h(x), it averages

\[
\cos(f(p),f(p-\alpha h(p)))
\]

over deterministically resized patches p. It is detector-training-free. [Paper Tables 2-4](https://arxiv.org/html/2511.14030v1) report mean AUROC 0.834 on Synthbuster, 0.946 on GenImage, and 0.934 on Deepfake-LSUN-Bedroom. Synthbuster DALL-E 3 is 0.422: a concrete failure, not universal separation. Typical settings use DINOv2 ViT-L/14, 16 or 36 patches, hence roughly 32 or 72 patch-view forwards/image. The [code repository](https://github.com/sungikchoi/WaRPAD) provides evaluation but no separate learned detector weights.

**Our analysis:** This directly occupies the idea of high-frequency perturbation response plus crop aggregation. Its score has a real-image direction; do not import the baselines' 0.5 threshold. The observed failure motivates testing sign/stability across generators without choosing the direction from test labels. CPU feasibility is limited by repeated large-backbone passes. Resolving the repository license and source-specific thresholds precedes code reuse or operating-point comparison.

### RIGID (2024 precursor): Start with the simplest prior art

The [paper](https://arxiv.org/abs/2405.20112) and [IBM code](https://github.com/IBM/RIGID) establish noise-response detection before RA-Det. Inspected snapshot `55af3cc2dc17f1f47aaba4720195eaca10226ca4` uses DINOv2 ViT-L/14 and clean/noisy cosine similarity, with Gaussian noise applied **after normalization**. Apache-2.0 code exists; no trained detection head is needed. The notebook calls CUDA directly. Its training-free status does not remove backbone dependence, noise-scale choices or threshold selection. It is a lower-cost conceptual control than RA-Det; a port to CPU or another backbone must be labeled an adaptation. The paper's headline improvement is not independently reproduced here.

### B-Free (CVPR 2025): Control the data before crediting the architecture

The [paper](https://openaccess.thecvf.com/content/CVPR2025/html/Guillaro_A_Bias-Free_Training_Paradigm_for_More_General_AI-generated_Image_Detection_CVPR_2025_paper.html) studies semantic/format/resolution shortcuts and reports improved generalization and calibration across 27 generators. The [official implementation](https://github.com/grip-unina/B-Free) trains a DINOv2-register detector with self-conditioned SD2.1 reconstructions and content augmentation, then uses large-crop inference. Reconstruction here constructs **training data**, unlike DID's per-input test-time reconstruction. Pretrained inference weights are linked in [code instructions](https://github.com/grip-unina/B-Free/blob/c6a9f898782fb466b29af01f21960b67415afb0e/code/README.md), with a published archive MD5. Weights were not transferred or tested. Its claims of semantic alignment do not eliminate every pipeline confound. Rebuilding the training corpus is costly and unnecessary for an initial pretrained comparison.

### WePe (NeurIPS 2025): Uncertainty as a detection signal

The [formal paper](https://papers.nips.cc/paper_files/paper/2025/hash/927dfe0d77fb20d9822bacd6737375a8-Abstract-Conference.html) treats model epistemic sensitivity as a proxy for generated content. [Technical details](https://openreview.net/pdf?id=5SqbLPaBww) describe perturbing pretrained encoder weights, comparing feature responses, and a trained variant distinct from the training-free form. Evaluation includes ImageNet/LSUN, GenImage and DRCT-2M with AUROC/AP. Our review establishes paper/code existence, not an independently audited performance ranking or a usable trained-variant checkpoint. **Our analysis:** high uncertainty may also describe unfamiliar real photographs; an authenticity score is not automatically a confidence estimate of another detector's correctness.

### ReSIDe (2026 preprint; author-announced acceptance): Direct reliability prior art

The [preprint](https://arxiv.org/html/2605.08574v1) freezes the detector, constructs intermediate-layer centroid-based logits, and learns a weighted confidence aggregation on held-out validation data. Its preference objective ranks correct above incorrect predictions. Reported experiments use GenImage-derived ResNet50/Swin-T detectors under six shifts, measuring risk-coverage/AURC; the abstract reports **up to 69.55% AURC reduction**, not average detection-accuracy gain. No official runnable implementation was established in this review. **Our analysis:** post-hoc is not parameter-free: centroids and aggregation need reference/validation data. The reported comparisons do not establish transfer to the selected ProGAN-trained CNNDetection/UniversalFakeDetect checkpoints or to the exact R2 generator/source mixture. “Add abstention” or “aggregate intermediate confidence” is already occupied territory.

## 7. Answers to the four research questions

| Question | What existing evidence supports | What remains a testable question, not a TrueSight finding |
| --- | --- | --- |
| A. Stable perturbation-response difference? | RIGID, RA-Det, WaRPAD and WePe report response differences under particular encoders/probes. | Does separation persist after matching content, codec, resolution, and processing history? Does it predict errors on unseen sources rather than merely source identity? Is its sign stable without test-label correction? |
| B. Reconstruction as additional evidence? | DIRE/DID establish reconstruction-based representations and repeated residuals. | Does residual evidence improve conditional performance beyond existing scores at matched FPR and compute? Does benefit survive a different reconstruction model, repeated seeds, and processing controls? It is not a new independent observation of reality. |
| C. Transferable common features? | Cross-source benchmark results and DoU's diversity objective support useful transfer over evaluated sources. | Which cues survive generator-family and real-source shifts simultaneously? Are cues complementary after nuisance controls, or redundant outputs of the same backbone? No reviewed result guarantees a universal invariant. |
| D. Recognize insufficient evidence? | ReSIDe explicitly studies abstention; B-Free studies calibration; WePe supplies a different uncertainty-based authenticity score. | Can a confidence rule fitted without target-generator labels rank errors on a new generator and new real-source pipeline? Does it protect both classes without rejecting almost everything? |

These are bounded gaps suggested by the review. An absence in this selected literature is not proof of worldwide novelty. Before claiming an algorithmic contribution, perform a dedicated prior-art search on the exact proposed mechanism and evaluation setting.

## 8. Candidate opportunities and falsification tests

All items below are **our hypotheses**, not approved algorithms or demonstrated innovations.

1. **Response evidence for selective reliability under compound shift.** Ask whether fixed perturbation responses add error-ranking information beyond native score margin and ordinary test-time disagreement. Compare random rejection, native confidence, disagreement, RIGID/WaRPAD response and, if reproducible, ReSIDe. Success requires lower paired AURC and lower selective error at prespecified coverage on held-out generators and a second real-source pipeline. Failure includes gains disappearing after codec controls, after equal-forward-pass controls, or outside one source. This goes beyond merely adding a rejection option, but novelty remains unverified.
2. **When reconstruction differencing actually helps.** Measure residual covariance and seed sensitivity, then evaluate incremental evidence conditional on original detector scores. Compare r1, r2, r1-r2 and compute-matched repeated first-order residuals. A hypothesis is that benefit concentrates where reconstruction noise is sufficiently correlated. Reject it if the gain is only threshold tuning or image-format leakage. Generating second-order residuals or fusing them with a CNN is already DID, not a new algorithm.
3. **Useful diversity versus nuisance diversity.** Compare cue/error correlations and effective rank before and after controlled format/content changes, with matched capacity and data. A new regularizer would need to improve held-out performance or reliability beyond DoU and simple ensembles, not merely decorrelate features. Learning weights on the evaluation generators would invalidate the intended generalization claim.

For selective prediction, distinguish the classifier from the acceptance rule:

\[
C(t)=P(q(x)\ge t),\qquad
R(t)=P(\hat y(x)\ne y\mid q(x)\ge t).
\]

Report the risk-coverage curve, AURC, class-conditional coverage, accepted-sample FPR/FNR and rejected-sample error rate. Rejection is not a prediction of “real.” Fixed-coverage test curves are descriptive; a deployable threshold must be selected separately. Vanilla calibration or conformal guarantees cannot be assumed under arbitrary generator/source shift. A stronger authenticity detector and a stronger error-ranking rule are separate achievements.

## 9. TrueSight feasibility and protocol boundaries

The audited machine has an i5-10210U, about 7.8 GiB RAM, Intel UHD graphics and no detected CUDA GPU. Its earlier free-disk measurement was about 45.7 GiB, not a current allocation. No local throughput or memory benchmark has been run.

| Route | Detector training needed now? | Practical fit and barriers |
| --- | --- | --- |
| R2 CNNDetection + UniversalFakeDetect | No, with official weights | Keep the approved starting point. Small CPU technical trials may be possible; CLIP memory/runtime must be measured. |
| RIGID-style fixed response | No additional task training | Simplest future behavior control: about two encoder forwards/probe. Official large-backbone CUDA assumptions need adaptation; a smaller encoder is a distinct experiment. |
| WaRPAD | No additional task training | Best named recent candidate for a training-free extension; repeated patch forwards make remote GPU preferable. License, threshold and deterministic resizing need attention. |
| DoU pretrained evaluation | No new training if released weight works | The most accessible of the three requested trained methods for inference. CLIP plus intermediate cues/prompts, stochastic sampling, checkpoint coverage, and incomplete training release are barriers. Remote single-GPU feasibility must be measured; CPU support is not a speed guarantee. |
| DID full detector | Requires supplied trained branch weights or new classifier training | Two diffusion reconstructions dominate cost; remote GPU and a reproducible reconstruction configuration are needed. Published A800 timing does not establish minimum VRAM. Not the first local experiment. |
| RA-Det full reproduction | Learned prober and heads required | Highest immediate barrier: detector weights not located, source/config discrepancies, multi-GPU training recipe. Study the idea without claiming that a simple noise probe reproduces RA-Det. |
| B-Free pretrained / WePe | No full retraining for pretrained/training-free variants | Useful later controls; large backbone passes and licenses still matter. Rebuilding B-Free data or training WePe's adapted variant is outside the present preference. |
| ReSIDe-style reliability analysis | Detector frozen; reference/validation fitting needed for full method | Low parameter count is attractive, but needs new splits, feature storage, implementation verification and more than a tiny diagnostic set. |

The R2 **80-image technical trial remains pipeline-only**. The **600-image main experiment remains exploratory**, with four sources and 75 images/class/source. This review does not add frontier models to that frozen comparison or authorize execution. Existing R2 test images must not become development data for a new confidence rule. A later research protocol needs disjoint development/validation, held-out generator evaluation and an external real-source check, with content groups kept together. Four sources cannot provide strong evidence of universality or precise low-FPR guarantees; reserve independent data before tuning.

## 10. Recommended discussion order, not an algorithm decision

Study **RA-Det, DID and DoU** to understand three contrasting mechanisms: learned behavioral probing, repeated reconstruction evidence, and representation diversity. Read **WaRPAD/RIGID** before designing a low-cost response experiment, and **ReSIDe** before proposing any rejection mechanism. For actual first implementation, retain R2; a later fixed-response comparison is the lowest-cost research extension, not a final choice of algorithm.

The user and ChatGPT should decide: whether the next scientific target is authenticity accuracy or error-aware abstention; whether to obtain remote GPU access; which nuisance controls and independent real sources are feasible; whether missing checkpoints justify postponement; and how to reserve development and final test sources before learning any fusion or confidence rule. Independent contribution is an eventual objective. It has not been achieved or established by this review.
