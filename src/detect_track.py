import cv2
import time
import math
import os
import pandas as pd
from ultralytics import YOLO

# ==============================
# PATHS
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VIDEO_PATH = os.path.join(BASE_DIR, "..", "videos", "heavy-traffic-noise-in-India.mp4")
OUTPUT_VIDEO = os.path.join(BASE_DIR, "..", "output", "annotated_video.mp4")
OUTPUT_CSV = os.path.join(BASE_DIR, "..", "output", "violations.csv")

# ==============================
# CONFIGURATION
# ==============================

CONF_THRESHOLD = 0.4
VEHICLE_CLASSES = [2, 3, 5, 7]  # car, bike, bus, truck

PIXEL_TO_METER = 0.05
SPEED_LIMIT = 80
PARKING_SPEED_LIMIT = 15
PARKING_TIME_SEC = 4

# ==============================
# INITIALIZATION
# ==============================

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(VIDEO_PATH)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

out = cv2.VideoWriter(
    OUTPUT_VIDEO,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height)
)

start_time = time.time()
total_frames = 0

prev_positions = {}
low_speed_counter = {}
violation_logs = []

# ==============================
# MAIN LOOP (SAFE EXIT)
# ==============================

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        total_frames += 1

        results = model.track(
            frame,
            persist=True,
            classes=VEHICLE_CLASSES,
            conf=CONF_THRESHOLD
        )

        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            ids = results[0].boxes.id.cpu().numpy()
            classes = results[0].boxes.cls.cpu().numpy()  # ✅ ADDED

            timestamp = total_frames / fps

            for box, track_id, cls_id in zip(boxes, ids, classes):
                x1, y1, x2, y2 = map(int, box)
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                track_id = int(track_id)

                vehicle_type = model.names[int(cls_id)]  # ✅ ADDED

                speed_kmph = 0

                # ==============================
                # SPEED CALCULATION
                # ==============================
                if track_id in prev_positions:
                    px, py = prev_positions[track_id]
                    dist_px = math.sqrt((cx - px)**2 + (cy - py)**2)
                    dist_m = dist_px * PIXEL_TO_METER
                    speed_kmph = dist_m * fps * 3.6

                prev_positions[track_id] = (cx, cy)

                # ==============================
                # OVER-SPEEDING
                # ==============================
                if speed_kmph > SPEED_LIMIT:
                    violation_logs.append([
                        round(timestamp, 2),
                        track_id,
                        vehicle_type,          # ✅ ADDED
                        "Over-Speeding",
                        round(speed_kmph, 2)
                    ])

                    cv2.putText(
                        frame,
                        f"{vehicle_type} Overspeed {int(speed_kmph)} km/h",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 255),
                        2
                    )

                # ==============================
                # ILLEGAL PARKING
                # ==============================
                if speed_kmph <= PARKING_SPEED_LIMIT:
                    low_speed_counter[track_id] = low_speed_counter.get(track_id, 0) + 1
                else:
                    low_speed_counter[track_id] = 0

                parked_time = low_speed_counter[track_id] / fps

                if parked_time >= PARKING_TIME_SEC:
                    violation_logs.append([
                        round(timestamp, 2),
                        track_id,
                        vehicle_type,          # ✅ ADDED
                        "Illegal Parking",
                        round(speed_kmph, 2)
                    ])

                    cv2.putText(
                        frame,
                        f"{vehicle_type} Illegal Parking",
                        (x1, y2 + 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 255),
                        2
                    )

        annotated = results[0].plot()
        out.write(annotated)

        cv2.imshow("Traffic Monitoring System", annotated)
        if cv2.waitKey(1) & 0xFF == 27:
            break

except KeyboardInterrupt:
    print("\nStopped by user. Saving progress...")

finally:
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    elapsed = time.time() - start_time
    avg_fps = total_frames / elapsed if elapsed > 0 else 0

    df = pd.DataFrame(
        violation_logs,
        columns=[
            "Time(sec)",
            "Vehicle_ID",
            "Vehicle_Type",     # ✅ ADDED
            "Violation_Type",
            "Speed(km/h)"
        ]
    )

    df.to_csv(OUTPUT_CSV, index=False)

    print("================================")
    print("Frames Processed:", total_frames)
    print("Average FPS:", round(avg_fps, 2))
    print("CSV saved:", OUTPUT_CSV)
    print("================================")
