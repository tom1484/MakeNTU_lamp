from tflite_runtime.interpreter import Interpreter
import cv2
from os import path
import numpy as np


class RoadObjectDetector:
    def __init__(self, lamp_spec) -> None:
        self.position = lamp_spec["position"]

        # data_folder = "./TFLite_BBD"
        data_folder = "./TFLite_SSD"
        self.model_path = path.join(data_folder, "detect.tflite")
        self.label_path = path.join(data_folder, "labelmap.txt")

        with open(self.label_path, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]
        if self.labels[0] == '???':
            del(self.labels[0])

        
        self.interpreter = Interpreter(self.model_path)
        print("Model Loaded Successfully.")

        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        self.floating_model = (self.input_details[0]['dtype'] == np.float32)
        self.input_height, self.input_width = self.input_details[0]['shape'][1:3]
        self.input_mean, self.input_std = 127.5, 127.5
        print(f"Image Shape: ({self.input_width}, {self.input_height})")
    
    def detect(self, frame):
        cap_height, cap_width = frame.shape[:2]
        frame_resized = cv2.resize(frame, (self.input_width, self.input_height))
        frame_RGB = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        input_data = np.expand_dims(frame_RGB, axis=0)

        if self.floating_model:
            input_data = (np.float32(input_data) - self.input_mean) / self.input_std

        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()

        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]

        detections = []
        bbox_frame = np.zeros(frame.shape, dtype=np.uint8)
        for i in range(len(scores)):
            # print(self.labels[int(classes[i])])
            if (scores[i] > 0.7) and (scores[i] <= 1.0) and (int(classes[i]) in [0, 2]):
                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1, boxes[i][0] * cap_height))
                xmin = int(max(1, boxes[i][1] * cap_width))
                ymax = int(min(cap_width, boxes[i][2] * cap_height))
                xmax = int(min(cap_width, boxes[i][3] * cap_width))
                
                cv2.rectangle(bbox_frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)

                # Draw label
                object_name = self.labels[int(classes[i])] # Look up object name from "labels" array using class index
                label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                cv2.rectangle(bbox_frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                cv2.putText(bbox_frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text

                object = {
                    'type': object_name, 
                    'position': self.position
                    }
                detections.append(object)

        return bbox_frame, detections