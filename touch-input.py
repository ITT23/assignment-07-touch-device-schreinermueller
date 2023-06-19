
import cv2
import cv2.aruco as aruco
import sys
#import mediapipe as mp

video_id = 2

if len(sys.argv) > 1:
    video_id = int(sys.argv[1])


# Create a video capture object for the webcam
cap = cv2.VideoCapture(video_id)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('sides.avi',fourcc, 20.0, (640, 480))
# out = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))
#cap = cv2.VideoCapture('C:/Users/sinas/ITTCode/assignment-07-touch-device-schreinermueller/img_corner_1.avi')
# mpHands = mp.solutions.hands
# hands = mpHands.Hands()s
# mpDraw = mp.solutions.drawing_utils

res_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
res_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(res_height, res_width)
fingertip = None
while True:
    # success, image = cap.read()
    # imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # results = hands.process(imageRGB)


    # Capture a frame from the webcam
    ret, frame = cap.read()
    #cv2.imshow("frame", frame)
    out.write(frame)
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, 90, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_contours = cv2.drawContours(img_contours, contours, -1, (255, 0, 0), 3)
    print(hierarchy)

    max_x = 0
    for contour in contours:
        for point in contour:
            x, y = point[0]
            if 30 < x < res_width -30 and 30 < y < res_height-30:
                #print("border")
                if x > max_x:
                    #print("max")
                    max_x = x
                    fingertip = (x, y)

    if fingertip is not None:
        #print("marker")
        img_marker = cv2.drawMarker(img_contours,
                                    fingertip,
                                    (0, 255, 0),
                                    markerType=cv2.MARKER_CROSS)
        bounding_box = [(fingertip[0]-60, fingertip[1]-30), (fingertip[0], fingertip[1]+30)]

        print(frame.shape)
        box = frame[fingertip[1]-30:fingertip[1]+30, fingertip[0]-60:fingertip[0]]#, :]#, fingertip[1]-30:fingertip[1]+30]
        print(box.shape)
        #box_gray = cv2.cvtColor(box, cv2.COLOR_BGR2GRAY)
        #ret, box_thresh = cv2.threshold(box_gray, 70, 255, cv2.THRESH_BINARY)
        # wenn die meisten punkte in der bounding box nach diesem threshold weiß sind, ist es hovern
        #img_rectangle = cv2.rectangle(img_marker, (fingertip[0]-60, fingertip[1]-30), (fingertip[0], fingertip[1]+30), (0, 255, 0), 3)
        #cv2.imshow('frame', box_thresh)
    # Display the frame
    cv2.imshow('frame', img_contours)

    # Wait for a key press and check if it's the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
out.release()
cv2.destroyAllWindows()


