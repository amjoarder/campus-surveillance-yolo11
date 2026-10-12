# Model checkpoints

The object and aggressive-actor checkpoints are distributed through the repository's GitHub release assets. Their filenames and SHA-256 checksums are recorded in `manifest.json`. Place them at `implementation/object_detection/best.pt` and `implementation/behavior_detection/best.pt` for application execution.

The checkpoints use the stock Ultralytics/PyTorch serialization. Use the documented dependency versions and load model files only from trusted sources. Third-party Ultralytics license requirements apply.
