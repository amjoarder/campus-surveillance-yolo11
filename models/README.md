# Original checkpoints

Download `object_best.pt` and `behavior_best.pt` from the repository's v1.0.0 release. They are byte-identical to the supplied original `best.pt` files; SHA-256 values are recorded in `manifest.json`. No retraining, conversion, serialization, loading or inference was performed to prepare this release.

For the original implementation, place them as `implementation/object_detection/best.pt` and `implementation/behavior_detection/best.pt`. Stock Ultralytics/PyTorch serialization is retained. Use the documented dependency versions and only load model files from a trusted source. Third-party Ultralytics license requirements continue to apply.
