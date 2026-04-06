# 🚦 Traffic Monitoring System (AI-Based)

An AI-powered traffic monitoring system that detects **overspeeding vehicles** and **illegal parking violations** using YOLOv8 object detection and tracking — all in a single unified pipeline.

---

## 📌 Features

- 🚗 Real-time vehicle detection (Cars, Motorcycles, Buses, Trucks)
- 🏎️ Overspeeding detection with speed estimation
- 🅿️ Illegal parking detection using behavioral logic (speed + duration)
- 🎥 Annotated output video generation
- 📊 CSV violation report with vehicle type included
- 🧠 Works with moving camera footage (no static background required)

---

## 🛠️ Tech Stack

| Tool                 | Purpose                                |
| -------------------- | -------------------------------------- |
| Python               | Core programming language              |
| OpenCV               | Video processing & frame annotation    |
| YOLOv8 (Ultralytics) | Real-time vehicle detection & tracking |
| NumPy                | Numerical computation                  |
| Pandas               | Violation data logging & CSV export    |

---

## 📂 Project Structure

```
Traffic Monitoring System/
│── src/
│   ├── detect_track.py       # Main pipeline: detection, tracking & violation logic
│   ├── speed_violation.py    # Speed calculation utility module
│
│── videos/
│   ├── heavy-traffic-noise-in-India.mp4   # Input traffic video
│
│── output/
│   ├── annotated_video.mp4   # Output video with bounding boxes & violation labels
│   ├── violations.csv        # Detailed violation log
│
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/MuhammadAsad29/Traffic-Monitoring-System.git
cd traffic-monitoring-system

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

---

## ▶️ Run

```bash
python src/detect_track.py
```

---

## 🧠 How It Works

### 1. 🚗 Vehicle Detection & Tracking

YOLOv8 detects vehicles frame-by-frame and assigns each a **unique tracking ID** that persists across frames. Detected classes include: `car`, `motorcycle`, `bus`, `truck`.

### 2. 🏎️ Speed Estimation

Speed is calculated using **pixel displacement** between consecutive frames:

```
Speed (km/h) = Pixel Distance × PIXEL_TO_METER × FPS × 3.6
```

> `PIXEL_TO_METER = 0.05` (calibration assumption — mention in report)

### 3. ⚠️ Overspeeding Detection

If a vehicle's estimated speed exceeds **80 km/h**, a violation is recorded and annotated on the video in red.

### 4. 🅿️ Illegal Parking Detection

A vehicle is flagged as **illegally parked** if:

- Its speed remains **≤ 15 km/h**
- This persists for a duration of **≥ 4 seconds**

No polygon zone is required — detection is purely **behavioral**, making it robust for moving camera footage.

---

## 📊 Output

### 🎥 Annotated Video (`output/annotated_video.mp4`)

- Bounding boxes around all detected vehicles
- Speed and vehicle type labels per vehicle
- Red violation text for overspeeding & illegal parking

### 📄 CSV Report (`output/violations.csv`)

| Time(sec) | Vehicle_ID | Vehicle_Type | Violation_Type  | Speed(km/h) |
| --------- | ---------- | ------------ | --------------- | ----------- |
| 0.17      | 13         | motorcycle   | Over-Speeding   | 89.06       |
| 4.00      | 5          | car          | Illegal Parking | 5.4         |
| 17.73     | 281        | bus          | Over-Speeding   | 103.87      |

---

## 🎓 Key Idea — Moving Camera Support

Traditional parking detection systems rely on **background subtraction**, which completely fails when the camera is moving. This system overcomes that by:

- Defining illegal parking using **behavioral logic** (low speed sustained over time)
- Requiring **no static background** or fixed reference frame
- Making the system reliable in **real-world traffic scenarios**

---

## ⚙️ Configuration Parameters

| Parameter               | Value   | Description                            |
| ----------------------- | ------- | -------------------------------------- |
| `CONF_THRESHOLD`      | 0.4     | Minimum YOLOv8 detection confidence    |
| `SPEED_LIMIT`         | 80 km/h | Threshold for overspeeding violation   |
| `PARKING_SPEED_LIMIT` | 15 km/h | Max speed to qualify as parked         |
| `PARKING_TIME_SEC`    | 4 sec   | Min duration to flag illegal parking   |
| `PIXEL_TO_METER`      | 0.05    | Pixel-to-meter scale conversion factor |

---

## 🚀 Future Work

- [ ] Lane detection integration
- [ ] ANPR (Automatic Number Plate Recognition)
- [ ] Traffic analytics dashboard
- [ ] Real-time alert / notification system
- [ ] Calibrated pixel-to-meter mapping using reference objects

---

## 👨‍💻 Author

**Muhammad Asad**

---

## ⭐ Note

> This project is developed for academic purposes as part of the **CCP (Computing Concepts & Programming)**.
