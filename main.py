from threading import Thread
import cv2
import json
from time import time
from detector import RoadObjectDetector
from connection import Connection
import LiFi as lf
from LiFi import LED_IO


lamp_spec = json.loads(open("lamp.json", "r").read())
map = json.loads(open("map.json", "r").read())

roadObjectDetector = RoadObjectDetector(lamp_spec)
connection = Connection(lamp_spec)
ledIO = LED_IO(18)


bbox_frame, detections = None, []
detecting = False
def detect(frame):
    global bbox_frame, detections
    global detecting

    frame, detections = roadObjectDetector.detect(frame)
    if len(detections) > 0:
        print(f"\nDetected: {detections}\n")
        ret = connection.update_detection(detections)
        # print(ret)

    bbox_frame = frame    
    detecting = False


fetching = False
road_objects = []
def fetch_object():
    global fetching
    road_objects = connection.fetch_object()
    print(road_objects)

    # road_objects, map["roads"]
    data = [0, 0, len(road_objects), len(map["roads"])]
    for object in road_objects:
        data.append(object["position"][0])
        data.append(object["position"][1])

    for road in map["roads"]:
        data.append(road[0][0])
        data.append(road[0][1])
        data.append(road[1][0])
        data.append(road[1][1])
        data.append(road[2])

    ledIO.output(data)

    fetching = False


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
    
    
    if not fetching:
        fetching = True
        Thread(target=lambda: fetch_object()).start()

    cv2.imshow("img", frame)
    if cv2.waitKey(1) == ord('q'):
        break
