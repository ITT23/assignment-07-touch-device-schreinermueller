import cv2
import numpy as np
from DIPPID_sender import Event
import socket, json
from pynput.mouse import Button

class TouchInput:
    IP = '127.0.0.1'
    PORT = 5700
    def __init__(self):
        self.event = Event()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cap = cv2.VideoCapture('videos/dragging.avi')
        self.res_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.res_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


    def handle_sensordata(self, data):
        print(data)
        self.mouse.position = (10, 20)
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)


    def normalize(self, x, y):
        if self.res_height > 0 and self.res_width > 0:
            x = x/self.res_width
            y = y/self.res_height

        return x, y

    def calc_thresholds(frame_gray, tolerance):
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(frame_gray)
        print("maxval: " + str(max_val))
        print("minval: " + str(min_val))

        threshold = ((max_val + min_val) // 2) - tolerance

        return threshold
    
    # from https://stackoverflow.com/questions/11782147/python-opencv-contour-tree-hierarchy-structure
    def median_canny(self, img, thresh1, thresh2):
        median = np.median(img)
        img = cv2.Canny(img, int(thresh1 * median), int(thresh2 * median))
        return img


    def touch_or_hover(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        median = np.median(img)
        print(median)
        if int(median) < 70:
            return "hover"
        else:
            return "touch"


    def touch_input(self, dt):

        ret, frame = self.cap.read()
        
        # from https://stackoverflow.com/questions/11782147/python-opencv-contour-tree-hierarchy-structure
        blue, green, red = cv2.split(frame)
        # Run canny edge detection on each channel
        blue_edges = self.median_canny(blue, 0.2, 0.3)
        green_edges = self.median_canny(green, 0.2, 0.3)
        red_edges = self.median_canny(red, 0.2, 0.3)

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
                    if w >= 50 and h > 30:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                        cv2.circle(frame, (int(x+(w/2)), int(y+(h/2))), 5, (255, 0, 0), 3)
                        bounding_box = frame[y:y+h, x:x+w]
                        if bounding_box.size > 0:
                            # Display the bounding box image
                            inputType = self.touch_or_hover(bounding_box)

                        x, y = self.normalize(x+(w/2), y+(h/2))
                        event.update(x, y, inputType)

            message = json.dumps(event.eventsDict)
            self.sock.sendto(message.encode(), (self.IP, self.PORT))





