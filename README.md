# Campus Surveillance with Object and Aggressive-Actor Detection

Implementation code, training records, dataset provenance and numerical checks for the submitted YOLO11-based campus-surveillance study. The manuscript and its Overleaf source are provided separately.

![Proposed system architecture](assets/system_architecture.svg)

*Proposed system architecture. The diagram includes conceptual stages that are not implemented in the evaluated frame-based application; the scope and implemented path are documented in the manuscript.*

## Scope

The application runs independent YOLO11-large object and aggressive-actor detectors on decoded video frames and combines their outputs into four visible cue states. It records annotated video and decision logs, with frame images saved when an aggressive-actor cue is present. The application does not construct temporal sequences or confirm intent, violence or property damage.

Reported metrics are image-level localization measurements on the available task exports. Recording-identifier and cross-task image overlap are documented; the repository does not claim independent incident-level validation or operational performance.

## Repository structure

| Path | Contents |
|---|---|
| [`implementation/`](implementation/) | Video inference application and execution instructions |
| [`training/`](training/) | Recorded Ultralytics CLI commands, arguments, histories and code screenshots |
| [`datasets/`](datasets/) | Dataset versions, split counts, provenance and label-only manifests |
| [`models/`](models/) | Checkpoint hashes and retrieval instructions |
| [`campus_study/`](campus_study/) | Image-level results, overlap audits and verification scripts |
| [`tools/`](tools/) | Source integrity and cue-rule checks |
| [`assets/system_architecture.svg`](assets/system_architecture.svg) | Author-supplied proposed system diagram |

## Verification

The verification scripts run on Python 3.10 or later. They validate source hashes, Python syntax, training records, dataset manifests and numerical summaries without loading weights or running inference.

```bash
python tools/verify_release.py
python campus_study/code/verify_current_study.py
```

## Execution

See [`implementation/README.md`](implementation/README.md) for dependencies, model placement, input-video setup and output paths. Full execution requires the trained weights and an authorized video. The verification workflow does not execute the application.

## Training and data

Training used the Ultralytics 8.3.116 command-line interface. The command records, saved configurations, screenshots and epoch histories are included; no separate author-written training script was retained. Dataset source versions, split counts, annotation provenance and access restrictions are documented in [`datasets/README.md`](datasets/README.md). The repository contains manifests and annotation records, not participant-image pixels or video footage. Checkpoint hashes and access information are documented in [`models/README.md`](models/README.md).

## Citation

Software citation metadata are provided in [`CITATION.cff`](CITATION.cff).
