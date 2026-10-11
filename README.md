# Original campus-surveillance implementation

Code and dataset companion for the research of Ajmain Muhtady Joarder, Zannatul Tasmia Moyury, Jubayer Al Mahmud, Md. Alam Hossain and M. F. Mridha. Corresponding author: ja.mahmud@just.edu.bd.

This repository contains the actual integrated YOLO11 application, original training commands, saved training records, original checkpoint identities, dataset provenance and reproducible numerical analyses. **The manuscript, bibliography, paper diagrams, paper PDF and Overleaf source ZIP are not hosted here.** The authors receive the Overleaf project separately.

| Material | Location |
|---|---|
| Unchanged original integrated application | [implementation/main.py](implementation/main.py) |
| Run instructions and original output limitations | [implementation/README.md](implementation/README.md) |
| Actual historical training CLI commands and screenshots | [training/](training/) |
| Exact dataset versions, counts and export hashes | [datasets/](datasets/) |
| Original trained-weight hashes | [models/manifest.json](models/manifest.json) |
| Completed numerical results and later analysis tools | [campus_study/](campus_study/) |
| Original weights and label-only archives | [v1.0.0 release](https://github.com/amjoarder/campus-surveillance-yolo11/releases/tag/v1.0.0) |

## Verify without training or inference

```
python tools/verify_release.py
python campus_study/code/verify_current_study.py --root campus_study
python tools/cue_availability.py
```

These checks use Python 3.10+ and its standard library. GitHub Actions verifies original-code byte identity, source hashes, saved training selection, all 350 completed external clip records, 10000 paired-camera scene resamples, ten class-level AP rows and joint-cue counts. CI never imports the original application, loads a checkpoint, trains a model or performs detector inference.

## Original work and later assessment

The original implementation used the campus behavior export and the merged object collection. Training was performed through the Ultralytics 8.3.116 CLI, as shown by the original screenshots. No separate historical training notebook has been invented. Original application execution requires its documented directory layout, the original weights, an authorized input video and the GUI/inference dependencies.

**AIRTLab was not used in the original thesis implementation, training or checkpoint selection.** Its records here belong to an additional post-hoc fixed-weight assessment conducted during manuscript preparation. Three preselected frames per clip and the unchanged 0.5 threshold were used. Those outputs are secondary screening measurements, not validation of a live campus deployment. The stopped exhaustive-frame run is excluded.

The campus image splits have recording and cross-task overlap. The completed image-test AP50/AP50:95 values are 78.84/55.75% for objects and 87.69/52.90% for behavior. Post-hoc external OR screening has balanced accuracy 52.32% (95% scene-cluster interval 46.54–57.88%). Neither result establishes independent incident recognition or camera-hour false-alert rates.

## Data and model access

The release provides original weights and original labels/YAML/split-name manifests without image pixels. These annotation packages are not standalone image datasets. Full imagery is obtained from the credited source versions or the corresponding author, subject to source terms and participant permissions. Campus footage and third-party image pixels are not mirrored.

See [NOTICE.md](NOTICE.md) for rights and dependency provenance. The associated manuscript remains unpublished; no journal acceptance or DOI is claimed. Use `CITATION.cff` to cite this software/data-record release.
