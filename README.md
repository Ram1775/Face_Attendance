# Face Authentication Attendance System

## Overview
This project implements a real-time face authentication system for attendance marking.
It supports face registration, authentication, punch-in, punch-out, and basic spoof prevention.

## Technologies Used
- OpenCV (camera handling)
- Face Recognition (dlib / FaceNet embeddings)
- Python
- CSV for attendance storage

## Model and Approach
- Pre-trained FaceNet embeddings are used.
- Faces are converted into 128-D feature vectors.
- Euclidean distance is used for matching.
- Threshold = 0.6

## Training Process
- No training from scratch.
- User registers face using webcam.
- Face embeddings are stored locally.

## Spoof Prevention
- Eye blink detection
- Motion consistency across frames

## Accuracy Expectations
- Good lighting: ~95%
- Low lighting: ~80%
- Occlusion: Reduced accuracy

## Known Failure Cases
- Identical twins
- Poor lighting
- Masked faces
- Printed photo with fake motion

## How to Run
1. Register Face:
