# Image-level evaluation records

This directory contains the numerical records and audits used to report detector localization results and the limits of the available image partitions. The manuscript and supplementary files are supplied separately.

Run the reproducibility check from the repository root:

```bash
python campus_study/code/verify_current_study.py
```

The checker verifies the ten-class object AP table, behavior and object evaluation summaries, training-log checkpoint selection, and the ten-image paired cue diagnostic. It does not load model weights or perform inference.

`evidence/` contains saved training arguments and histories, image-evaluation summaries, annotation and recording-overlap audits, and source provenance. `supplementary_data/Supplementary_Data_1.csv` gives per-class object metrics. `Supplementary_Data_2.json` records the available recording-identifier linkage.

These records describe the supplied image exports. Recording overlap means they do not establish performance on unseen recordings or independently held-out incidents.
