import math
import pandas as pd

PIXEL_TO_METER = 0.05   # Assumption (mention in report)
SPEED_LIMIT = 60        # km/h

prev_positions = {}
violations = []

def check_speed(track_id, cx, cy, fps, timestamp):
    if track_id in prev_positions:
        px, py = prev_positions[track_id]
        distance_pixels = math.sqrt((cx-px)**2 + (cy-py)**2)
        distance_m = distance_pixels * PIXEL_TO_METER
        speed_mps = distance_m * fps
        speed_kmph = speed_mps * 3.6

        if speed_kmph > SPEED_LIMIT:
            violations.append([
                timestamp, track_id, "Over-Speeding", round(speed_kmph, 2)
            ])

    prev_positions[track_id] = (cx, cy)

def save_speed_violations():
    df = pd.DataFrame(
        violations,
        columns=["Time", "Vehicle_ID", "Violation", "Speed(km/h)"]
    )
    df.to_csv("../output/violations.csv", index=False)
