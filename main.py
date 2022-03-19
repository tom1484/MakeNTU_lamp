from threading import Thread
import cv2
import json
from time import time, sleep
from detector import RoadObjectDetector
from connection import Connection
import LiFi as lf
from LiFi import LED_IO


# load physical specification
lamp_spec = json.loads(open("lamp.json", "r").read())
map = json.loads(open("map.json", "r").read())

roadObjectDetector = RoadObjectDetector(lamp_spec)
connection = Connection(lamp_spec)
ledIO = LED_IO(17)


bbox_frame, detections = None, []
detecting = False
def detect(frame):
    global bbox_frame, detections
    global detecting

    # detect objects and update database
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
    global road_objects
    global fetching

    road_objects = connection.fetch_object()

    sleep(0.001)
    fetching = False


def LiFiSend():
    data = [lamp_spec["position"][0], lamp_spec["position"][1], len(road_objects), len(map["roads"])]
    
    # add road objects into LiFi data
    for object in road_objects:
        data.append(object["position"][0])
        data.append(object["position"][1])

    # add map information into LiFi data
    for road in map["roads"]:
        data.append(road[0][0])
        data.append(road[0][1])
        data.append(road[1][0])
        data.append(road[1][1])
        data.append(road[2])

    ledIO.output(data)


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # start detecting if previous thread ends
    if not detecting:
        detecting = True
        Thread(target=lambda: detect(frame)).start()
    
    # draw bounding boxes on frame
    if bbox_frame is not None:
        frame[bbox_frame > 0] = 0
        frame += bbox_frame
        # cv2.imshow("img", bbox_frame)
    
    # start fetching if previous thread ends
    if not fetching:
        fetching = True
        Thread(target=lambda: fetch_object()).start()
    
    # send LiFi signal
    LiFiSend()

    cv2.imshow("img", frame)
    if cv2.waitKey(1) == ord('q'):
        break
