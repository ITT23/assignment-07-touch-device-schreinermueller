import os
import pyglet
from pyglet import shapes, clock
import sys
from unistroke_model import UniStroke
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
window = pyglet.window.Window(fullscreen=True)

# later: drawn points are saved here
line = []

# init of lstm
recognizer = UniStroke()

sensor = SensorUDP(5700)


# can quit window with q / esc(?)
@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.Q:
        touchInput.cap.release()
        sys.exit(0)


# if mouse is released predict gesture and start an application
@window.event
def on_mouse_release(x, y, button, modifiers):
    window.clear()
    if pyglet.window.mouse.LEFT:
        prediction = recognizer.predict_gesture(recognizer.model_32, recognizer.encoder, line)
        # if gesture is recognized as one of the 3 defined, start the corresponding application
        for gesture in gestures:
            if prediction == gesture:
                path = paths[gestures.index(gesture)]
                os.startfile(path)
        line.clear()


# if gesture is drawn by mouse draw the current point
@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & pyglet.window.mouse.LEFT:
        line.append([int(x), int(y)])
        point = shapes.Circle(x, y, radius=5, color=(255, 225, 255))
        point.draw()

# if gesture is drawn by touch input use this method
def handle_sensordata(dt):
    if not sensor.get_value('events') is None:
        for eventIdx in sensor.get_value('events'):
            event = sensor.get_value('events')[eventIdx]
            if event['type'] == "touch":
                # scale x and y for the pyglet window
                x = float(event['x']) * window.width
                y = float(event['y']) * window.height
                # do the same as with the mouse input
                line.append([x, y])
                point = shapes.Circle(x, y, radius=5, color=(255, 225, 255))
                point.draw()
            # if finger is moving away from the glass predict a gesture
            elif event['type'] == 'hover':
                if len(line) >= 10:
                    window.clear()
                    if pyglet.window.mouse.LEFT:
                        prediction = recognizer.predict_gesture(recognizer.model_32, recognizer.encoder, line)
                        # if gesture is recognized as one of the 3 defined, start the corresponding application
                        for gesture in gestures:
                            if prediction == gesture:
                                path = paths[gestures.index(gesture)]
                                os.startfile(path)
                        line.clear()

# init of DIPPID-sender and touch-detector
touchInput = TouchInput()
clock.schedule_interval(touchInput.touch_input, 0.1)
# receive DIPPID events
clock.schedule_interval(handle_sensordata, 0.3)

pyglet.app.run()




