from threading import Thread
import cv2
import json
from time import time
from detector import RoadObjectDetector
from connection import Connection


lamp_spec = json.loads(open("lamp.json", "r").read())
map = json.loads(open("map.json", "r").read())

roadObjectDetector = RoadObjectDetector(lamp_spec)
connection = Connection(lamp_spec)


bbox_frame, detections = None, []
detected, detecting = False, False
def detect(frame):
    global bbox_frame, detected, detecting

    frame, detections = roadObjectDetector.detect(frame)
    if len(detections) > 0:
        print(detections)
        ret = connection.update_detection(detections)
        print(ret)

        detected = True

    bbox_frame = frame    
    detecting = False


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    if not detecting:
        detecting = True
        Thread(target=lambda: detect(frame)).start()
    
    if bbox_frame is not None:
        frame += bbox_frame
        # cv2.imshow("img", frame)
    
    # detections, map["roads"]

    cv2.imshow("img", frame)
    if cv2.waitKey(1) == ord('q'):
        break
