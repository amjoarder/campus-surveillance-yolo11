# Datasets and annotation provenance

The authors curated campus frames and annotated captured images by hand using Roboflow. Downloaded object images were already annotated and were merged with the author-prepared collection. Scripted campus recordings are not actual violent incidents.

| Collection | Train | Validation | Test | Total |
|---|---:|---:|---:|---:|
| Author-prepared object export v3 | 2154 | 200 | 103 | 2457 |
| Retained third-party object export v6 | 8312 | 666 | 327 | 9305 |
| Merged ten-class object export | 10466 | 866 | 430 | 11762 |
| Author-prepared behavior export v1 | 804 | 230 | 115 | 1149 |

Source versions:
- Authors' object project: https://universe.roboflow.com/hello-iorxu/harmful-object-detection/dataset/3
- Authors' behavior project: https://universe.roboflow.com/hello-iorxu/violent-behavior-detection/dataset/1
- Third-party object source: https://universe.roboflow.com/try-6siwu/thirdvision-with-blunt-objects-without-sumpak/dataset/6

The object author export contains 718 training source-name groups with three variants each. Its 2457 exported images must not be described as 2457 independent original campus photographs. The behavior export has one foreground class (`violent`), 593 images with a box and 556 empty-label background images. Its intended box target is only the person acting aggressively.

The release contains **original labels, dataset YAML/README files, and split image-name manifests without image pixels**, extracted from the two supplied ZIP exports. These are annotation packages, not standalone image datasets. Original mixed box/polygon rows are preserved. The object image test preserved each five-field box and separately converted polygon rows to enclosing boxes. Original full export hashes and exact label hashes are in `export_manifest.json`; no archive has been silently rebuilt or relabeled.

Obtain full imagery from the identified source versions, subject to their terms, or request the exact archived exports from the corresponding author: ja.mahmud@just.edu.bd. Local exports can differ from an online re-export; verify the archived hashes when reproducing the exact study. Campus imagery is not reuploaded here. Five exact object test pixel duplicates were excluded from the reported 425-image test; manifests identify the evaluated images. Recording overlap and cross-task image overlap remain and are documented in the paper and evidence files. Use recording-disjoint splits for a new study.

Export metadata identify CC BY 4.0 for the two authors' Roboflow projects. The third-party source retains its own metadata and attribution. Metadata licensing does not replace participant-image permissions. AIRTLab is not mirrored; its pinned revision and source hashes are in `campus_study/evidence/external_manifest.json`.
