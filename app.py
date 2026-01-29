import tkinter as tk
from tkinter import simpledialog, messagebox
import cv2
import os
import numpy as np
from PIL import Image, ImageTk
from attendance import mark_attendance
import time

# ------------------ LOAD FACE DETECTOR ------------------

detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
if detector.empty():
    raise RuntimeError("Haarcascade XML not found")

# ------------------ TKINTER SETUP ------------------

root = tk.Tk()
root.title("Face Authentication Attendance System")
root.geometry("850x650")

video_label = tk.Label(root)
video_label.pack(pady=10)

status_label = tk.Label(root, text="Choose an option", font=("Arial", 14))
status_label.pack(pady=10)

# ------------------ GLOBAL STATE ------------------

cap = None
mode = None            # "register" or "attendance"
username = None
img_count = 0
MAX_IMAGES = 25

recognizer = None
label_map = {}
recognized = False
recognition_time = None
AUTO_STOP = 4  # seconds

# ------------------ LOAD TRAINING DATA ------------------

def load_recognizer():
    global recognizer, label_map

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces = []
    labels = []
    label_map = {}
    label_id = 0

    if not os.path.exists("faces"):
        return False

    for person in os.listdir("faces"):
        person_path = os.path.join("faces", person)
        if not os.path.isdir(person_path):
            continue

        label_map[label_id] = person
        for img in os.listdir(person_path):
            image = cv2.imread(os.path.join(person_path, img),
                               cv2.IMREAD_GRAYSCALE)
            if image is not None:
                faces.append(image)
                labels.append(label_id)
        label_id += 1

    if faces:
        recognizer.train(faces, np.array(labels))
        return True

    return False

# ------------------ CAMERA LOOP ------------------

def start_camera(selected_mode):
    global cap, mode, img_count, recognized, recognition_time

    mode = selected_mode
    img_count = 0
    recognized = False
    recognition_time = None

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Camera not accessible")
        return

    if mode == "register":
        status_label.config(text=f"Registering: {username}")
    else:
        status_label.config(text="Scanning face for attendance")

    update_frame()

def update_frame():
    global cap, img_count, recognized, recognition_time

    if cap is None:
        return

    ret, frame = cap.read()
    if not ret:
        stop_camera("Camera error")
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]

        # ---------- REGISTER MODE ----------
        if mode == "register":
            os.makedirs(f"faces/{username}", exist_ok=True)
            img_count += 1
            cv2.imwrite(f"faces/{username}/{img_count}.jpg", face)

            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
            status_label.config(text=f"Capturing face {img_count}/{MAX_IMAGES}")

            if img_count >= MAX_IMAGES:
                stop_camera("Registration complete")
                return

        # ---------- ATTENDANCE MODE ----------
        elif mode == "attendance" and recognizer is not None:
            label, confidence = recognizer.predict(face)

            if confidence < 70 and not recognized:
                name = label_map[label]
                status = mark_attendance(name)

                recognized = True
                recognition_time = time.time()
                status_label.config(text=f"{name} | {status}")

                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

            elif confidence >= 70:
                status_label.config(text="Unknown person")
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)

    # Display frame
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)
    imgtk = ImageTk.PhotoImage(image=img)

    video_label.configure(image=imgtk)
    video_label.image = imgtk

    # Auto stop after recognition
    if recognized and time.time() - recognition_time > AUTO_STOP:
        stop_camera("Attendance marked")
        return

    root.after(10, update_frame)

def stop_camera(msg):
    global cap
    if cap:
        cap.release()
        cap = None
    status_label.config(text=msg)
    root.after(2000, root.destroy)

# ------------------ BUTTON ACTIONS ------------------

def register_user():
    global username
    username = simpledialog.askstring("Register", "Enter your name:")
    if not username:
        return
    start_camera("register")

def start_attendance():
    if not load_recognizer():
        messagebox.showwarning("Warning", "No registered users found")
        return
    start_camera("attendance")

# ------------------ UI BUTTONS ------------------

btn_frame = tk.Frame(root)
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="Register Face",
          width=20, command=register_user).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="Start Attendance",
          width=20, command=start_attendance).grid(row=0, column=1, padx=10)

tk.Button(btn_frame, text="Exit",
          width=20, command=root.destroy).grid(row=0, column=2, padx=10)

root.mainloop()
