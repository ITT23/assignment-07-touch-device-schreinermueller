# task 2
import pyglet
from pyglet import clock
import sys
from MultitouchGame import MultitouchGame
from DIPPID import SensorUDP
from task_03.TouchInput import TouchInput

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

# fullscreen window
window = pyglet.window.Window(fullscreen=True)

move_array = []

# here coordinates start left bottom corner
touch = pyglet.shapes.Circle(0, 0, 5, color=(255, 0, 0))
finger_one = pyglet.shapes.Circle(0, 0, 5, color=(0, 255, 0))
finger_two = pyglet.shapes.Circle(0, 0, 5, color=(0, 255, 0))



def handle_sensordata(data):
    print(data)


sensor.register_callback('events', handle_sensordata)


#check if finger is in an image
def in_image(point):
    images = [game.stairsSprite, game.tablesSprite, game.windowsSprite]
    x = point[0]
    y = point[1]
    for image in images:
        if image.x <= x <= image.x + image.width and image.y <= y <= image.y + image.height:
            return image
    return None


def update(dt):

    if len(sensor.get_value('events')) > 0:
        # move
        if len(sensor.get_value("events")) == 1:
            sensor_x = float(sensor.get_value("events")["0"]["x"])
            sensor_y = float(sensor.get_value("events")["0"]["y"])
            x = int(sensor_x * window.width)
            y = int(sensor_y * window.height)
            touch.x = x
            touch.y = y
            sprite = in_image((x, y))
            dist_x = 0
            dist_y = 0
            if len(move_array) == 0:
                move_array.append((x, y))
            else:
                move_array.append((x, y))
                dist_x = move_array[0][0] - move_array[1][0]
                dist_y = move_array[0][1] - move_array[1][1]
                move_array.pop(0)

            if sprite is not None:
                # hier quasi funktion für move
                sprite.x = sprite.x + dist_x
                sprite.y = sprite.y + dist_y

        # resize or rotate
        if len(sensor.get_value("events")) == 2:
            finger_coordinates = []
            for event_num in range(len(sensor.get_value("events"))):
                sensor_x = float(sensor.get_value("events")[str(event_num)]["x"])
                sensor_y = float(sensor.get_value("events")[str(event_num)]["y"])
                x = int(sensor_x * window.width)
                y = int(sensor_y * window.height)
                finger_coordinates.append((x, y))
            #print(finger_coordinates)
            finger_one.x = finger_coordinates[0][0]
            finger_one.y = finger_coordinates[0][1]
            finger_two.x = finger_coordinates[1][0]
            finger_two.y = finger_coordinates[1][1]



# # fullscreen window
# window = pyglet.window.Window(fullscreen=True)

game = MultitouchGame()

@window.event
def on_draw():
    window.clear()
    game.draw()
    touch.draw()
    finger_one.draw()
    finger_two.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.Q:
        sys.exit(0)

# init of DIPPID-sender and touch-detector
touchInput = TouchInput()
clock.schedule_interval(touchInput.touch_input, 0.05)

pyglet.clock.schedule_interval(update, 0.01)
pyglet.app.run()
