from sqlite3 import connect
import cv2
import json
from detector import RoadObjectDetector
from connection import Connection


lamp_spec = json.loads(open("lamp.json", "r").read())

roadObjectDetector = RoadObjectDetector(lamp_spec)
connection = Connection(lamp_spec)


cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame, detections = roadObjectDetector.detect(frame)
    if len(detections) > 0:
        print(detections)
        ret = connection.update_detection(detections)
        print(ret)


    cv2.imshow('img', frame)
    if cv2.waitKey(1) == ord('q'):
        break


