import os
import pyglet
from pyglet import shapes, clock
import sys
from unistroke_model import UniStroke
from pynput.mouse import Button, Controller
from DIPPID import SensorUDP
from TouchInput import TouchInput



# get applications and gestures from text file
gestures = []
paths = []

with open('applications.txt') as f:
    file = f.readlines()

for line in file:
    shape, path = line.split(" ", 1)
    gestures.append(shape)
    path = path.rstrip('\n')
    paths.append(path)


# pyglet application
title = "GestureRecognition"
window = pyglet.window.Window(fullscreen=True)#1000, 500, title)

# later: drawn points are saved here
line = []

# init of lstm
recognizer = UniStroke()

# init of mouse controller for touch input -> triggers mouse click
mouse = Controller()

sensor = SensorUDP(5700)

def handle_sensordata(dt):
    for eventIdx in sensor.get_value('events'):
        event = sensor.get_value('events')[eventIdx]
        if event['type'] == "touch":
            mouse.position = (float(event['x']) * window.width, float(event['y']) * window.height)
            mouse.press(Button.left)
            #mouse.release(Button.left)


# can quit window with q (?)
@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.Q:
        touchInput.cap.release()
        #cv2.destroyAllWindows()
        sys.exit(0)


# if mouse is released predict gesture and start an application
@window.event
def on_mouse_release(x, y, button, modifiers):
    window.clear()
    print("mouse release")
    if pyglet.window.mouse.LEFT:
        prediction = recognizer.predict_gesture(recognizer.model_32, recognizer.encoder, line)
        # if gesture is recognized as one of the 3 defined, start the corresponding application
        for gesture in gestures:
            if prediction == gesture:
                path = paths[gestures.index(gesture)]
                os.startfile(path)
        line.clear()


# if gesture is drawn draw the current point
@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    print("mouse drag")
    if buttons & pyglet.window.mouse.LEFT:
        line.append([int(x), int(y)])
        point = shapes.Circle(x, y, radius=5, color=(255, 225, 255))
        point.draw()

touchInput = TouchInput()
clock.schedule_interval(touchInput.touch_input, 0.1)

clock.schedule_interval(handle_sensordata, 0.1)

pyglet.app.run()




