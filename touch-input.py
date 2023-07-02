import cv2
import sys
import time

import numpy

from DIPPID_sender import Event
import socket, time, json



IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

video_id = 1

if len(sys.argv) > 1:
    video_id = int(sys.argv[1])

counter = 0


# Create a video capture object for the webcam
cap = cv2.VideoCapture(video_id)
cap = cv2.VideoCapture('videos/hover.avi')

res_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
res_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


# for writing videos
#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#out = cv2.VideoWriter('videos/scale.avi',fourcc, 20.0, (640, 480))


def normalize(x, y):
    if res_height > 0 and res_width > 0:
        x = x/res_width
        y = y/res_height

    return x, y

if (cap.isOpened()== False): 
  print("Error opening video stream or file")


# from https://stackoverflow.com/questions/11782147/python-opencv-contour-tree-hierarchy-structure
def median_canny(img):
    median = numpy.median(img)
    thresh_val = abs(140 - median)*0.02
    thresh_val = thresh_val+0.05
    return thresh_val, median


def touch_or_hover(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (255, 255, 0), 1)
    cv2.imshow('img finger', img)
    mean = numpy.mean(img)
    print(mean)
    if int(mean) < 80:
        return "hover"
    else:
        return "touch"


while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    if counter > 100:

        #out.write(frame)
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if counter == 101:
            thresh_val, median = median_canny(img_gray)

        # from https://stackoverflow.com/questions/11782147/python-opencv-contour-tree-hierarchy-structure
        blue, green, red = cv2.split(frame)
        # Run canny edge detection on each channel
        blue_edges = cv2.Canny(blue, thresh_val*median, (thresh_val+0.2)*median)
        green_edges = cv2.Canny(green, thresh_val*median, (thresh_val+0.2)*median)
        red_edges = cv2.Canny(red, thresh_val*median, (thresh_val+0.2)*median)

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
                    if 300 > w > 50 and 300 > h > 30:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                        cv2.circle(frame, (int(x+(w/2)), int(y+(h/2))), 5, (255, 0, 0), 3)
                        bounding_box = frame[y:y+h, x:x+w]
                        if bounding_box.size > 0:
                            # Display the bounding box image
                            inputType = touch_or_hover(bounding_box)

                        x, y = normalize(x+(w/2), y+(h/2))
                        event.update(x, y, inputType)

            if len(event.eventsDict["events"]) < 5:
                message = json.dumps(event.eventsDict)
                print(message)
                sock.sendto(message.encode(), (IP, PORT))

        cv2.imshow("frame", frame)

    counter += 1
    time.sleep(0.03)

    # Wait for a key press and check if it's the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
#out.release()
cv2.destroyAllWindows()


