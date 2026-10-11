# Unchanged original integrated implementation

`main.py` is the original file, including its commented earlier version. SHA-256: `8382785ab5267eeee46c3db9f22c909f871469aaffa0b22b78199dc2a7d2b33f`. It was not refactored or replaced. A byte-identical archival copy appears under `campus_study/code/original_integrated.py` for integrity verification.

Original behavior: sequential object and behavior prediction on a stretched 640x640 frame; confidence threshold 0.5; additional class-agnostic object NMS at IoU 0.4; four displayed cue states; annotated AVI, frame decision log and unannotated original JPEGs when a behavior cue is present. It uses OpenCV windows and runs immediately when executed or imported.

Run on an authorized machine with Python 3.10 and the inference dependencies in `requirements-inference.txt`. PyTorch and CUDA installation must match that machine; the historical environment was PyTorch 2.6.0+cu124 with Ultralytics 8.3.116. No historical full dependency lock was retained, so this requirements file is a compatible execution specification, not an invented historical lock.

1. Download the original release weights and place them at `implementation/object_detection/best.pt` and `implementation/behavior_detection/best.pt`.
2. Put an authorized input video at `implementation/test_videos/VID_20250412_160230.mp4`, or intentionally change the `VIDEO_PATH` constant for your own run. No campus video is redistributed.
3. Create `implementation/output` **before running**; the original script creates alerts/log directories but does not create the output directory.
4. Change the working directory to `implementation`, then execute `python main.py`. The original output is `output/result8.avi`; press the documented OpenCV quit key to stop.

The original source retains automatic device selection. It is not run by CI or during publication preparation. A new run can consume GPU/CPU resources, and these instructions do not authorize running it on the authors' laptop.

The original text `Normal: No threat detected` is an interface string, not a validated safety judgment. `frames_with_objects` increments once per detection and is an instance counter; its historical value is not accuracy. The reported average FPS omits parts of full pipeline timing and is not claimed as complete-video throughput. Original text-only run outputs are preserved under `original_run_records/`.
