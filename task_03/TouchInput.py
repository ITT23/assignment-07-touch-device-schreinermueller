import cv2
import numpy as np
import socket, json
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from DIPPID_sender import Event

class TouchInput:
    IP = '127.0.0.1'
    PORT = 5700
    def __init__(self):
        self.event = Event()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cap = cv2.VideoCapture(1)
        self.res_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.res_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.counter = 0
        self.thresh_val = 0
        self.median = 0


    def normalize(self, x, y):
        if self.res_height > 0 and self.res_width > 0:
            x = x/self.res_width
            y = y/self.res_height

        return x, y

    
    # from https://stackoverflow.com/questions/11782147/python-opencv-contour-tree-hierarchy-structure
    def median_canny(self, img):
        median = np.median(img)
        thresh_val = abs(140 - median) * 0.02
        thresh_val = thresh_val + 0.05

        return thresh_val, median


    def touch_or_hover(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        median = np.median(img)
        if int(median) < 70:
            return "hover"
        else:
            return "touch"


    def touch_input(self, dt):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            frame = cv2.flip(frame, 1)

            if self.counter > 100:

                # out.write(frame)
                img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if self.counter == 101:
                    self.thresh_val, self.median = self.median_canny(img_gray)

                # from https://stackoverflow.com/questions/11782147/python-opencv-contour-tree-hierarchy-structure
                blue, green, red = cv2.split(frame)
                # Run canny edge detection on each channel
                blue_edges = cv2.Canny(blue, self.thresh_val * self.median, (self.thresh_val + 0.2) * self.median)
                green_edges = cv2.Canny(green, self.thresh_val * self.median, (self.thresh_val + 0.2) * self.median)
                red_edges = cv2.Canny(red, self.thresh_val * self.median, (self.thresh_val + 0.2) * self.median)

                # Join edges back into image
                edges = blue_edges | green_edges | red_edges
                contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                if hierarchy is not None and len(hierarchy) != 0:
                    hierarchy = hierarchy[0]  # get the actual inner list of hierarchy descriptions
                    event = Event()
                    # For each contour, find the bounding rectangle and draw it
                    for component in zip(contours, hierarchy):
                        currentContour = component[0]
                        currentHierarchy = component[1]
                        x, y, w, h = cv2.boundingRect(currentContour)
                        inputType = ""
                        if currentHierarchy[3] < 0:
                            # these are the outermost parent components
                            # print(w)
                            if 300 > w > 50 and 300 > h > 30:
                                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                                cv2.circle(frame, (int(x + (w / 2)), int(y + (h / 2))), 5, (255, 0, 0), 3)
                                bounding_box = frame[y:y + h, x:x + w]
                                if bounding_box.size > 0:
                                    # Display the bounding box image
                                    inputType = self.touch_or_hover(bounding_box)

                                x, y = self.normalize(x + (w / 2), y + (h / 2))
                                event.update(x, y, inputType)

                    if len(event.eventsDict["events"]) < 5:
                        message = json.dumps(event.eventsDict)
                        print(message)
                        self.sock.sendto(message.encode(), (self.IP, self.PORT))

            self.counter += 1
