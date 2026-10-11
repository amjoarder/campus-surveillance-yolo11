# Paper analyses

These scripts were prepared during manuscript analysis, after the original training and integrated implementation. They are not the original authors' training scripts.

Python 3.10+ standard library is sufficient:
```
python campus_study/code/verify_current_study.py --root campus_study
python campus_study/code/analyze_transfer.py --records campus_study/evidence/external_clip_records --manifest campus_study/evidence/external_manifest.json --output transfer_recomputed.json
```

The verifier checks all 350 saved clip-record hashes, sampled frame indices, four cue rules, paired-camera groups, 10000 scene bootstrap replicates, original checkpoint-selection epochs, ten class-level AP rows and original-code byte identity. It does not repeat detector inference. The evidence files preserve original record wording and paths; terms such as `recovered` in archival JSON describe the earlier file audit, not a new dataset or invented experiment.

Supplementary Data 1 is per-class object results; Data 2 is external screening and uncertainty; Data 3 is recording/source linkage. No incomplete exhaustive-frame results are included. Numerical reproducibility does not imply a recording-independent campus test or verify participant permissions.
