# R2: Public data feasibility

Reviewed: 2026-10-21. This is a source and metadata review, not an image-level audit. No dataset archives, model weights, or images were downloaded. The acquired image count is **zero**. Counts below distinguish published inventory from the proposed TrueSight sample.

## Recommendation

Use selected **AIGIBench test archives** for the first pilot, subject to the acquisition checks in the [draft protocol](protocol-r2.md). This provides one documented release covering the requested conditions without collecting new images. Prefer ProGAN as a seen-generator reference, StyleGAN3 as an unseen GAN candidate, GLIDE as an older diffusion candidate, and FLUX.1-dev as a relatively newer candidate. The last two are both diffusion-family conditions; “newer” is a relative date category, not a separate architecture or a claim to represent the latest generators in 2026.

Revision 0.2: start with an 80-image technical trial (10 real and 10 generated per source), separate from the retained 600-image exploratory main experiment. No model execution or large dataset download is part of this revision. Seen/unseen designations must be supported independently for each detector and exact checkpoint, including an explicit unresolved state; the shared descriptions below are preliminary, not a completed overlap audit.

## Sources, access, and restrictions

### AIGIBench — preferred

The [official repository](https://github.com/HorizonTEL/AIGIBench) links to [Hugging Face](https://huggingface.co/datasets/HorizonTEL/AIGIBench) and Baidu Netdisk. The Hugging Face metadata endpoint reported a public, ungated repository at revision `e44ec40efe5117a5ccdaa6ff0e89ed934d03d310`. Its file listing exposes these archives:

| Archive under `test/` | Compressed bytes | Planned real / generated images |
| --- | ---: | ---: |
| `ProGAN.zip` | 834652672 | 75 / 75 |
| `StyleGAN3.zip` | 7485360621 | 75 / 75 |
| `GLIDE.zip` | 2357075074 | 75 / 75 |
| `FLUX1-dev.zip` | 8778428543 | 75 / 75 |
| Total | 19455516910 | 300 / 300 |

The metadata listing is available through the [Hugging Face tree API](https://huggingface.co/api/datasets/HorizonTEL/AIGIBench/tree/main?recursive=true&limit=1000). A pinned file URL has the form `https://huggingface.co/datasets/HorizonTEL/AIGIBench/resolve/e44ec40efe5117a5ccdaa6ff0e89ed934d03d310/test/GLIDE.zip`. Only metadata accessibility was checked; successful full transfer, archive integrity, and eligible image counts remain unverified. The dataset viewer currently reports a generation error; this does not establish that ZIP files are broken.

The [dataset card](https://huggingface.co/datasets/HorizonTEL/AIGIBench/blob/main/README.md) declares CC BY-NC-SA 4.0. The [repository license](https://github.com/HorizonTEL/AIGIBench/blob/main/LICENSE) also includes dataset-specific noncommercial terms. Plan academic, noncommercial use with attribution; retain the terms and check subset-specific notices. Do not assume the release's blanket terms resolve all rights in upstream photographs or generated outputs. Publish manifests and measurements rather than repackaging images.

The [paper, v2](https://arxiv.org/html/2505.12335v2) reports 4,500 generated and 4,500 real GLIDE images. Its appendix describes prompt construction and CLIP-based filtering, which may influence comparisons with a CLIP detector. The repository notes corrections to paper test counts. We therefore do not treat paper counts as verified archive counts, or invent exact totals for the other selected archives. Real-image source identities, prompt relationships, and cross-folder duplication must be checked after acquisition. A shared release alone does not establish matched real controls.

### Synthbuster + RAISE-1k — useful follow-up

The [versioned Zenodo release](https://zenodo.org/records/10066460) reports 9,000 generated images: 1,000 each from nine generators, including SD 1.4, SDXL, and DALL-E 3. It provides prompts based loosely on RAISE-1k photographs. It supplies no GAN condition and does not include the real photographs. It is useful for a later comparison with better documented semantic relationships, rather than a mixed-source replacement for the entire pilot.

The [Zenodo metadata API](https://zenodo.org/api/records/10066460) identifies CC BY-NC-SA 4.0 and lists `synthbuster.zip` at 12,372,557,226 bytes, MD5 `0695bd328e16ea21c5c9cc2ae1d994ff`. The [official RAISE download page](https://loki.disi.unitn.it/RAISE/download.html) offers the 1,000-image subset separately and restricts use to noncommercial research and education with citation. RAISE contains raw photographs; a documented, consistent rendering pipeline is needed for RGB detectors. We did not verify full archive transfers or render any files.

### GenImage — reserve, not first choice

The [official README](https://github.com/GenImage-Dataset/GenImage/blob/main/Readme.md) lists Google Drive and Baidu download channels, eight generator settings, and ImageNet-derived real photographs. Its scale exceeds one million real/generated pairs, but the reviewed README does not establish a complete dataset-specific permission chain. A request for a root `LICENSE` file returned 404; this alone does not prove that no terms exist elsewhere. Verify the dataset and upstream ImageNet terms before use. Its older generator coverage and possible ImageNet pretraining exposure make it less suitable for the first newer-generator comparison. Third-party mirror licenses are not evidence of permission from the original rights holders.

## Detector compatibility and overlap

| Selected baseline | Documented task-training provenance | Implication for the pilot |
| --- | --- | --- |
| CNNDetection, official `blur_jpg_prob0.5.pth` | Official README describes LSUN real images and ProGAN images across 20 categories | ProGAN is a seen generator; the test files must still be held out. StyleGAN3, GLIDE, and FLUX are candidate unseen task-training generators. |
| UniversalFakeDetect, official CLIP ViT-L/14 with `fc_weights.pth` | Official README describes the ProGAN/LSUN training collection across 20 categories and a frozen-backbone linear classifier | Same seen/unseen distinction, pending verification of the exact checkpoint. CLIP pretraining exposure remains uncertain. |

Sources: [CNNDetection README](https://github.com/PeterWang512/CNNDetection), [UniversalFakeDetect README](https://github.com/WisconsinAIVision/UniversalFakeDetect). Do not use AIGIBench's retrained Setting-II checkpoints: those incorporate SD 1.4 and would change the training provenance. Earlier publication evaluation on a generator, such as GLIDE, is distinct from task-specific training on it; it still limits any claim that our test is historically untouched.

ProGAN images may be repackaged from existing benchmarks; a `test` directory name is not proof of independence from training. Before interpreting H2, establish original split provenance and check hashes against accessible training/validation manifests. If those manifests are unavailable, report sample overlap as unresolved; do not claim verified held-out performance or estimate a clean seen-to-unseen gap. For every other subset, record generator identity and exact checkpoint/version when available. ImageNet exposure for CNN backbones and web-image exposure for CLIP cannot be ruled out by checking detector task training alone.

Both detectors accept RGB images, but their native preprocessing differs. Preserve that difference in the initial comparison and document it; identical input files do not imply identical model inputs. Repository code licenses are also distinct: [CNNDetection](https://github.com/PeterWang512/CNNDetection/blob/master/LICENSE.txt) uses CC BY-NC-SA 4.0; [UniversalFakeDetect](https://github.com/WisconsinAIVision/UniversalFakeDetect/blob/main/LICENSE) uses MIT. Verify notices for weights and pretrained dependencies separately before acquisition.

## Feasibility decision

The four archives total about 19.46 GB compressed. **Do not download that collection now.** Prioritize lawful, reproducible acquisition of the 80 trial images, followed later by a disjoint main sample. Full extraction is not justified merely by the small requested sample. No HTTP metadata check guarantees future availability or quota-free transfer.

### Small-sample access investigation

Preferred routes, in order:

1. Use an official, versioned per-image endpoint or author-provided small subset if available. Require source-relative IDs, license notices, class and generator labels, and reproducible selection, rather than hand-picked examples. The inspected release tree exposes ZIP archives; an official per-image route for all four sources has not been established.
2. Investigate selective ZIP access through HTTP byte ranges. A HEAD-only request to the pinned `ProGAN.zip` URL returned HTTP 200, `Accept-Ranges: bytes`, and length 834652672. No image or archive payload was fetched. This is only a feasibility signal: HTTP 206 behavior, ZIP/ZIP64 central-directory access, per-member compression, server redirects, stable bytes/ETags, and range-transfer cost remain untested, including the other three archives. Do not present selective extraction as implemented or validated. A later bounded range probe must stop if the server ignores Range, returns the full file, or exceeds a declared transfer limit.
3. If selective access fails, seek an author-maintained small release or a clearly authorized mirror with verifiable correspondence to the original release. A mirror's own license label is insufficient. Contacting maintainers requires a separate user instruction; no message was sent in this task. Do not substitute untraceable previews, screenshots, or re-encoded viewer images.

Before a later selective transfer, declare a byte budget and request-size limits, verify authorization under the dataset and upstream terms, and record the access procedure. A ZIP route should enumerate original members from its directory, apply the protocol's deterministic selection to available metadata, and retain member paths, CRC checks, SHA-256 values, archive revision and byte length. Content grouping and matching may require additional metadata or samples; disclose that limit rather than claiming a score-blind random sample from an unknown full population. Never use selected image offsets as a substitute for provenance.

If none of these routes can supply traceable samples within the budget, stop acquisition and document a revised data choice. The full archives remain deferred. Freeze each stage's manifest after provenance, matching, and duplicate checks, before its scores are inspected. Match content categories, real-source composition, formats, resolutions, and processing histories as closely as available metadata permits, documenting unavoidable differences. No small-sample images have yet been obtained, and the two stages' acquired counts remain zero.
