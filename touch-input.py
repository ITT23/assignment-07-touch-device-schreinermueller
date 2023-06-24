import cv2
import sys
import time

def centroid(max_contour):
    moment = cv2.moments(max_contour)
    if moment['m00'] != 0:
        cx = int(moment['m10'] / moment['m00'])
        cy = int(moment['m01'] / moment['m00'])
        return cx, cy
    else:
        return None

video_id = 0#2

if len(sys.argv) > 1:
    video_id = int(sys.argv[1])


# Create a video capture object for the webcam
cap = cv2.VideoCapture(video_id)

# for writing videos
#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#out = cv2.VideoWriter('sides.avi',fourcc, 20.0, (640, 480))

cap = cv2.VideoCapture('sides.avi')

if (cap.isOpened()== False): 
  print("Error opening video stream or file")


while True:

    # Capture a frame from the webcam
    ret, frame = cap.read()
    print(ret, frame)

    #out.write(frame)
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, 80, 255, cv2.THRESH_BINARY) #90
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_contours = cv2.drawContours(img_contours, contours, -1, (255, 0, 0), 3)

    # calculate centroid -> can be deleted?
    if len(contours) > 0:
        max_cont = max(contours, key=cv2.contourArea)
        cnt_centroid = centroid(max_cont)
        circle_img = cv2.circle(img_contours, cnt_centroid, 5, [255, 255, 255], -1)

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

                cv2.imshow('frame', img_rectangle)
    if len(new_contours) > 0:
        img_contours = cv2.drawContours(frame, new_contours, -1, (255, 255, 255), 10)
        cv2.imshow('frame', img_contours)

    time.sleep(0.1)

    # Wait for a key press and check if it's the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
#out.release()
cv2.destroyAllWindows()


