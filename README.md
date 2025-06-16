# 👥 People Counter Cam 📹

🎥 A real-time people counting system using YOLOv8 + DeepSORT for tracking people entering and exiting a space via a camera feed.

It logs **daily counts** to Excel, tracks **peak entry hours**, and supports **24/7 monitoring** — perfect for entrances, lobbies, or small shops!

---

## 🚀 Features

✅ Real-time person detection with **YOLOv8**  
✅ Robust object tracking with **DeepSORT**  
✅ Directional line logic to detect **IN** / **OUT** movement  
✅ **Excel logs per day** with in/out count and **peak entry hour**  
✅ Supports **external or built-in cameras**  
✅ **Automatically resets at midnight**  
✅ Runs continuously — perfect for **home or office use**

---

## 🧠 How It Works (System Overview)

This project combines multiple components to enable a reliable 24/7 people counting system:

### 🧩 Components:
| Component | Role |
|----------|------|
| 🎯 **YOLOv8** | Detects all "person" objects in each frame. |
| 🔁 **DeepSORT** | Assigns each person a unique ID and tracks them across frames. |
| 📏 **Line-based Logic** | A virtual line is drawn in the frame. When a person crosses it, we decide IN or OUT based on movement direction. |
| 📊 **Pandas + Excel** | Stores daily logs with counts and the peak entry hour. |
| 🕒 **Time Monitoring** | At midnight, the current day’s data is saved and the counters reset automatically. |

### 🔄 Flow:
1. Capture live video from webcam (internal/external).
2. Detect people with YOLOv8.
3. Track movement across frames using DeepSORT IDs.
4. If someone crosses the line:
   - Top → Bottom: `IN`
   - Bottom → Top: `OUT`
5. Save time of entry for peak hour analysis.
6. Write daily data to Excel on day change or exit.

---

## ⚙️ How to Run

```
pip install opencv-python ultralytics deep_sort_realtime pandas openpyxl

python people_counter.py

```

## 📸 Sample Output

![screenshot](/sample_output.png)


## ⚠️ Challenges Faced

Despite the simplicity of the idea, real-time computer vision introduces several challenges:

### 🎥 1. Accurate Person Detection
Relying only on object detection (YOLO) is noisy — you may detect partially visible people, reflections, or misclassify objects.  
✅ **Solution**: Using **YOLOv8 + DeepSORT tracking** improves precision by maintaining person identity across frames.

---

### 🔄 2. Tracking Direction of Movement
Just knowing a person’s location isn’t enough — we need to know where they **came from** and where they **went**.  
✅ **Solution**: This is handled by storing the **last Y-coordinate** of each person (by their unique ID).

---

### 🕒 3. Daily Reset and Persistence
Real-time systems don’t stop — so we needed automatic **midnight resets** and **daily data logs** to avoid data accumulation or loss.  
✅ **Solution**: Code checks date and triggers log-save/reset automatically.

---

### 🔌 4. Hardware Limitations
Running YOLO models on low-end laptops or Raspberry Pi can cause performance drops.  
✅ **Solution**: Use the lightweight `yolov8n.pt` (Nano version) for efficient performance on modest devices.

---

## 🌐 Real-time Use Cases

This project can be directly applied in:

✅ 🏠 **Home entry tracking**  
✅ 🏢 **Office lobbies / gated entries**  
✅ 🏪 **Small shops / retail counters**  
✅ 🏫 **Classroom attendance approximation**  
✅ 🚶‍♂️ **Footfall analysis for events**

---

With enhancements, it could also support:

🚦 **Live dashboards**  
🔔 **Alert systems for over-crowding**  
🧠 **Smart building automation triggers**

## 🤝 Contributions

Feel free to fork, raise issues, or submit pull requests!

