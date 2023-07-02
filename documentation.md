# Documentation

Building Process / Design Decisions:
1. Assembling the hardware: We placed a camera in the middle (and at the bottom) of a cardboard box. On top of the box, we attached glass with a sheet of paper. To be able to access the cable of the camera, we poked a hole in one side of the box.
2. The next step was to be able to show an image of the camera. 
3. Detecting the fingertips and bounding boxes: We first tried a very basic variant of edge detection by converting the image to a grayscale image and thresholding. But this was not very robust, which was the reason we chose the canny edge detection for detecting the fingertips in an image. In order to use it in different lighting conditions, we first tested with our recorded videos and based on that we implemented a function that produces fitting values.
4. Distinguishing touch and hover: threshold value 70 to check the mean value of the frame in the bounding box. 
5. Sending DIPPID events: The events are sent in touch-input.py, but are converted into a dictionary / into the right structure in DIPPID_sender.py. Each detected touch or hover event in a frame is then sent via DIPPID.


Usage Guide: <br>
Default value for the video id of the camera is 2. If you want to test it with a recorded video, you can insert the path to the video instead of the video id in touch-input.py. To start the detection of the fingertips, run touch-input.py and place touch the glass surface. If you want to receive DIPPID events, you can also tun the DIPPID_receiver.py, which prints out a dictionary of the events that were detected in the current frame.