# Video inference application

`main.py` runs the submitted frame-based application. It loads separate YOLO11 object and aggressive-actor detectors, processes video frames at 640 × 640, combines the detections into four cue states, and writes annotated video, decision logs and behavior-triggered frame images. The application does not construct temporal sequences.

## Requirements

Use Python 3.10 with the dependencies in `requirements-inference.txt`. The saved training environment used Ultralytics 8.3.116 and PyTorch 2.6.0+cu124; install a PyTorch build compatible with the execution machine.

## Inputs and model files

1. Obtain the trained checkpoints from the repository's v1.0.0 release assets and place them at `object_detection/best.pt` and `behavior_detection/best.pt`.
2. Place an authorized video at `test_videos/VID_20250412_160230.mp4`, or edit `VIDEO_PATH` in `main.py`. Campus footage is not redistributed.
3. Create the `output/` directory before execution. The application creates `alerts/` and `logs/` as needed.

## Run

From this directory, execute:

```bash
python main.py
```

The application writes `output/result8.avi`, decision records under `logs/`, and behavior-triggered JPEG snapshots under `alerts/`. It opens an OpenCV display window and uses the quit key documented in the source to stop processing. Device selection is automatic. The verification workflow syntax-checks this file but does not execute it or load weights.

The displayed text `Normal: No threat detected` is an interface state, not a validated safety judgment. The `frames_with_objects` counter counts detections, not frames or accuracy. The saved FPS value omits parts of full pipeline timing and is not complete-video throughput. Text-only run records are in `original_run_records/`.
