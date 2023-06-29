import cv2
import sys
import time

import numpy

from DIPPID_sender import Event
import socket, time, json



IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

video_id = 2

if len(sys.argv) > 1:
    video_id = int(sys.argv[1])


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


def calc_thresholds(frame_gray, tolerance):
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(frame_gray)
    print("maxval: " + str(max_val))
    print("minval: " + str(min_val))

    threshold = ((max_val + min_val) // 2) - tolerance

    return threshold


# from https://stackoverflow.com/questions/11782147/python-opencv-contour-tree-hierarchy-structure
def median_canny(img, thresh1, thresh2):
    median = numpy.median(img)
    img = cv2.Canny(img, int(thresh1 * median), int(thresh2 * median))
    return img


def touch_or_hover(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    median = numpy.median(img)
    print(median)
    if int(median) < 70:
        return "hover"
    else:
        return "touch"


while True:

    # Capture a frame from the webcam
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    #print(ret, frame)

    #out.write(frame)
    #img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #threshold_value = calc_thresholds(img_gray, 30)
    #ret, thresh = cv2.threshold(img_gray, 80, 255, cv2.THRESH_BINARY)
    # from https://stackoverflow.com/questions/11782147/python-opencv-contour-tree-hierarchy-structure
    blue, green, red = cv2.split(frame)
    # Run canny edge detection on each channel
    blue_edges = median_canny(blue, 0.2, 0.3)
    green_edges = median_canny(green, 0.2, 0.3)
    red_edges = median_canny(red, 0.2, 0.3)

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
                        inputType = touch_or_hover(bounding_box)

                    x, y = normalize(x+(w/2), y+(h/2))
                    event.update(x, y, inputType)

        if len(event.eventsDict["events"]) < 5:
            message = json.dumps(event.eventsDict)
            print(message)
            sock.sendto(message.encode(), (IP, PORT))

        #print(message)

        #img_contours = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #img_contours = cv2.drawContours(img_contours, contours, -1, (255, 0, 0), 3)
        #print(hierarchy)
    cv2.imshow("frame", frame)

    '''
    new_contours = []
    for contour in contours:
            area = cv2.contourArea(contour)
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if radius > 30:
                continue
            center = (int(x), int(y))
            radius = int(radius)
            #circle_img = cv2.circle(img_contours, center, radius, (0,0,255), 2)
            if 50 >= area >= 10 and 50 >= radius >= 5:
                new_contours.append(contour)
                #cv2.imshow('frame', circle_img)
                img_rectangle = cv2.rectangle(frame, (int(x)-30, int(y)-30), (int(x)+30, int(y)+30), (0, 255, 0), 3)
                
                x, y = normalize(int(x), int(y))
                inputType = "touch"
                #event.update(x, y, inputType)
                #message = json.dumps({"events": event.eventsDict})
                #print(message)
                #sock.sendto(message.encode(), (IP, PORT))

                cv2.imshow('frame', img_rectangle)
    if len(new_contours) > 0:
        img_contours = cv2.drawContours(frame, new_contours, -1, (255, 255, 255), 10)
        #cv2.imshow('frame', img_contours)
        '''
    time.sleep(0.03)

    # Wait for a key press and check if it's the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
#out.release()
cv2.destroyAllWindows()


