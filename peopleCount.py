import cv2
import numpy as np
import pandas as pd
from datetime import datetime, date
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# Initialize YOLOv8 and DeepSORT
model = YOLO("yolov8n.pt")
tracker = DeepSort(max_age=30)

# Setup video capture (0 = laptop cam, 1 = external cam)
cap = cv2.VideoCapture(0)

# For virtual line crossing logic
ret, frame = cap.read()
frame_h, frame_w = frame.shape[:2]
line_y = frame_h // 2

# Daily stats
in_count = 0
out_count = 0
id_last_y = {}  # ID: last seen y position
entry_times = []  # timestamps of entries

# Excel logging
today_str = date.today().strftime('%Y-%m-%d')
excel_filename = f"people_log_{today_str}.xlsx"

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)[0]
    detections = []

    # YOLO detections to DeepSORT format
    for box in results.boxes:
        if int(box.cls[0]) == 0:  # class 0 = person
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            detections.append(([x1, y1, x2 - x1, y2 - y1], conf, 'person'))

    tracks = tracker.update_tracks(detections, frame=frame)

    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, w, h = track.to_ltrb()
        cx = int((l + l + w) / 2)
        cy = int((t + t + h) / 2)

        # Draw bounding box
        cv2.rectangle(frame, (int(l), int(t)), (int(l + w), int(t + h)), (0, 255, 0), 2)
        cv2.putText(frame, f"ID {track_id}", (int(l), int(t - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Check line crossing
        if track_id in id_last_y:
            prev_y = id_last_y[track_id]
            if prev_y < line_y and cy >= line_y:
                in_count += 1
                entry_times.append(datetime.now())
            elif prev_y > line_y and cy <= line_y:
                out_count += 1
        id_last_y[track_id] = cy

    # Draw line and stats
    cv2.line(frame, (0, line_y), (frame_w, line_y), (255, 255, 0), 2)
    cv2.putText(frame, f"In: {in_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 2)
    cv2.putText(frame, f"Out: {out_count}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 200), 2)

    cv2.imshow("People Counter", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# After camera stops – log data to Excel
data = {
    "Date": [today_str],
    "In Count": [in_count],
    "Out Count": [out_count],
    "Peak Entry Hour": [""]
}

# Calculate peak hour
if entry_times:
    hours = [dt.strftime('%H:00') for dt in entry_times]
    peak_hour = pd.Series(hours).value_counts().idxmax()
    data["Peak Entry Hour"] = [peak_hour]

# Save to Excel
df = pd.DataFrame(data)

try:
    existing = pd.read_excel(excel_filename)
    df = pd.concat([existing, df], ignore_index=True)
except FileNotFoundError:
    pass

df.to_excel(excel_filename, index=False)
print(f"\n✅ Day's data saved to {excel_filename}")
