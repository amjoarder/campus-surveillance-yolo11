import cv2
import time
import os
from ultralytics import YOLO
from collections import defaultdict

# --- Load Models ---
object_model = YOLO("object_detection/best.pt")
behavior_model = YOLO("behavior_detection/best.pt")

# --- Class Definitions ---
harmful_object_classes = [
    "baseball bat", "cricket bat", "crowbar", "hammer", "ice pick",
    "long knife", "pistol", "pocket-knife", "rifle", "stick"
]
behavior_class_name = "violent"

# --- Class-wise Colors ---
color_map = {
    "baseball bat": (255, 0, 0),
    "cricket bat": (0, 255, 255),
    "crowbar": (255, 255, 0),
    "hammer": (0, 128, 255),
    "ice pick": (255, 0, 255),
    "long knife": (128, 0, 128),
    "pistol": (0, 0, 255),
    "pocket-knife": (0, 255, 0),
    "rifle": (255, 128, 0),
    "stick": (0, 128, 128),
    "VIOLENT": (0, 255, 255)
}

# --- Accuracy Stats ---
metrics = {
    "total_frames": 0,
    "frames_with_violence": 0,
    "frames_with_objects": 0,
    "total_detections": defaultdict(int)
}
fps_list = []

# Create output folders
os.makedirs("alerts", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# --- Video Source ---
VIDEO_PATH = "test_videos/VID_20250412_160230.mp4"
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise IOError(f"Cannot open video file: {VIDEO_PATH}")

orig_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
orig_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
resized_w, resized_h = 640, 640

output_path = "output/result8.avi"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_path, fourcc, fps, (orig_w, orig_h))

prev_time = time.time()
frame_id = 0

# --- IoU Function for Manual NMS ---
def compute_iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou

def manual_nms(boxes, threshold=0.5):
    boxes = sorted(boxes, key=lambda b: b[5], reverse=True)
    keep = []
    while boxes:
        current = boxes.pop(0)
        keep.append(current)
        boxes = [b for b in boxes if compute_iou(current[:4], b[:4]) < threshold]
    return keep

# --- Main Loop ---
event_log = open("logs/event_log.txt", "w")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_id += 1
    metrics["total_frames"] += 1
    input_frame = cv2.resize(frame.copy(), (resized_w, resized_h))
    scale_x = orig_w / resized_w
    scale_y = orig_h / resized_h

    object_detections = []
    behavior_detected = False
    draw_boxes = []

    # --- Object Detection ---
    obj_result = object_model.predict(input_frame, verbose=False)[0]
    obj_boxes = []
    for box in obj_result.boxes:
        if box.conf[0] < 0.5:
            continue
        cls_id = int(box.cls.item())
        label = harmful_object_classes[cls_id] if cls_id < len(harmful_object_classes) else "Unknown"
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        x1, x2 = int(x1 * scale_x), int(x2 * scale_x)
        y1, y2 = int(y1 * scale_y), int(y2 * scale_y)
        obj_boxes.append((x1, y1, x2, y2, label, float(box.conf[0])))

    # --- Apply NMS ---
    nms_boxes = manual_nms(obj_boxes, threshold=0.4)
    for x1, y1, x2, y2, label, conf in nms_boxes:
        color = color_map.get(label, (0, 0, 255))
        draw_boxes.append((x1, y1, x2, y2, label, color))
        object_detections.append(label)
        metrics["total_detections"][label] += 1
        metrics["frames_with_objects"] += 1

    # --- Behavior Detection ---
    beh_result = behavior_model.predict(input_frame, verbose=False)[0]
    for box in beh_result.boxes:
        if box.conf[0] < 0.5:
            continue
        if int(box.cls.item()) == 0:
            behavior_detected = True
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            x1, x2 = int(x1 * scale_x), int(x2 * scale_x)
            y1, y2 = int(y1 * scale_y), int(y2 * scale_y)
            draw_boxes.append((x1, y1, x2, y2, "VIOLENT", color_map["VIOLENT"]))

    # --- Fusion Decision ---
    if behavior_detected:
        metrics["frames_with_violence"] += 1
        if object_detections:
            decision = f"WARNING: Violence + Object(s): {', '.join(object_detections)}"
        else:
            decision = "WARNING: Violent Behavior"
        cv2.imwrite(f"alerts/frame_{frame_id}.jpg", frame)
    elif object_detections:
        decision = f"Alert: Object(s) Detected - {', '.join(object_detections)}"
    else:
        decision = "Normal: No threat detected"
    event_log.write(f"Frame {frame_id}: {decision}\n")

    # --- Draw Boxes ---
    for x1, y1, x2, y2, label, color in draw_boxes:
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(frame, (x1, y1 - th - 10), (x1 + tw + 6, y1), color, -1)
        cv2.putText(frame, label, (x1 + 3, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # --- FPS ---
    current_time = time.time()
    fps_live = 1 / (current_time - prev_time)
    prev_time = current_time
    fps_list.append(fps_live)

    # --- Overlay Panel ---
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (orig_w, 100), (30, 30, 30), -1)
    frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
    cv2.putText(frame, decision, (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255, 255, 255), 2)
    cv2.putText(frame, f"FPS: {fps_live:.2f}", (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    out.write(frame)

# --- Final Accuracy Summary ---
cap.release()
out.release()
cv2.destroyAllWindows()
event_log.close()

with open("logs/metrics.txt", "w") as f:
    f.write(f"Total frames: {metrics['total_frames']}\n")
    f.write(f"Frames with violence: {metrics['frames_with_violence']}\n")
    f.write(f"Frames with objects: {metrics['frames_with_objects']}\n")
    f.write(f"Total object detections by class:\n")
    for label, count in metrics["total_detections"].items():
        f.write(f"  {label}: {count}\n")
    avg_fps = sum(fps_list) / len(fps_list)
    f.write(f"Average FPS: {avg_fps:.2f}\n")
