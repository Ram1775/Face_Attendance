import cv2
import os
import numpy as np
from attendance import mark_attendance
import time

detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []
label_map = {}
label_id = 0

for person in os.listdir("faces"):
    label_map[label_id] = person
    for img in os.listdir(f"faces/{person}"):
        image = cv2.imread(f"faces/{person}/{img}", cv2.IMREAD_GRAYSCALE)
        faces.append(image)
        labels.append(label_id)
    label_id += 1

recognizer.train(faces, np.array(labels))

cam = cv2.VideoCapture(0)

recognized_users = set()   # NEW
COOLDOWN_TIME = 5           # seconds

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces_detected = detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces_detected:
        face = gray[y:y+h, x:x+w]
        label, confidence = recognizer.predict(face)

        if confidence < 70:
            name = label_map[label]

            # Mark attendance only once
            if name not in recognized_users:
                status = mark_attendance(name)
                recognized_users.add(name)
                last_time = time.time()
            else:
                status = "Recorded"

            text = f"{name} | {status}"
            color = (0,255,0)
        else:
            text = "Unknown"
            color = (0,0,255)

        cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
        cv2.putText(frame,text,(x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,color,2)

    cv2.imshow("Face Attendance System", frame)

    # Auto exit after cooldown
    if recognized_users and time.time() - last_time > COOLDOWN_TIME:
        break

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()
