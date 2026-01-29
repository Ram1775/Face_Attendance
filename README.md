# Face Authentication Attendance System

## Overview
This project implements a **GUI-based Face Authentication Attendance System**
using **OpenCV** and **LBPH (Local Binary Patterns Histogram)**.
The system captures a user’s face through a live camera feed, authenticates
registered users, and automatically marks **Punch-IN / Punch-OUT** attendance.

The application is fully **GUI-driven** and does **not require any terminal
interaction** during normal usage.

---

## Key Features
- GUI-based desktop application (Tkinter)
- Face registration inside the application
- Real-time face authentication
- Automatic Punch-IN / Punch-OUT logic
- Unknown / unregistered face rejection
- Automatic camera stop after recognition
- Automatic application exit after attendance
- Offline and lightweight system

---

## Technologies Used
- **Python**
- **OpenCV**
- **Tkinter**
- **LBPH Face Recognizer**
- **NumPy**
- **Pandas**

---

## System Workflow
1. User opens the application (double-click executable or run script)
2. User registers face via GUI (name entered in popup)
3. Multiple face images are captured automatically
4. During attendance:
   - Camera opens
   - Face is detected and authenticated
   - Attendance is marked (IN / OUT)
   - Camera and application close automatically

---

## Model and Approach Used

### Face Detection
- Haar Cascade Classifier (OpenCV)
- Detects facial regions in real time

### Face Recognition
- Local Binary Patterns Histogram (LBPH)
- Texture-based facial feature extraction
- Histogram comparison for identity matching

LBPH is chosen because it:
- Works well with small datasets
- Handles lighting variations
- Is fast and suitable for real-time applications

---

## Training Process
- No external dataset is used
- Training data is collected live during registration
- ~25 facial images are captured per user
- Images are converted to grayscale and stored locally
- LBPH model is trained dynamically using registered faces

---

## Accuracy Expectations

| Condition | Expected Accuracy |
|--------|------------------|
| Good indoor lighting | 85–92% |
| Normal office lighting | 80–88% |
| Low lighting | 65–75% |
| Unknown user | Correctly rejected |

Accuracy depends on lighting conditions, camera quality, and face visibility.

---

## Known Failure Cases (ML Limitations)
- Very poor lighting conditions
- Heavy face occlusion (mask, scarf)
- Extreme face angles
- Identical twins or very similar faces
- Printed photo spoof under ideal lighting

These are inherent limitations of face recognition systems.

---

## Real-World Deployment
In real-life usage:
- The application is packaged as a **desktop executable**
- Users do not interact with the terminal
- The system can run in kiosk mode at entry points
- Attendance is recorded automatically upon face authentication

---

## How to Run (Development Mode)

```bash
pip install opencv-python opencv-contrib-python pillow numpy pandas
python app.py
