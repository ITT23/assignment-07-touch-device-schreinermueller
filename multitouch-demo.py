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
resize_rotate_array = []

# here coordinates start left bottom corner
touch = pyglet.shapes.Circle(0, 0, 5, color=(255, 0, 0))
finger_one = pyglet.shapes.Circle(0, 0, 5, color=(0, 255, 0))
finger_two = pyglet.shapes.Circle(0, 0, 5, color=(0, 255, 0))

sprite_corners = []


def handle_sensordata(data):
    print(data)


sensor.register_callback('events', handle_sensordata)


def update(dt):
    global move_array
    global resize_rotate_array
    game.get_sprite_corners()

    if len(sensor.get_value('events')) > 0:
        # move

        if len(sensor.get_value("events")) == 1:
            sensor_x = float(sensor.get_value("events")["0"]["x"])
            sensor_y = float(sensor.get_value("events")["0"]["y"])
            x = int(sensor_x * window.width)
            y = int(window.height - sensor_y * window.height)
            touch.x = x
            touch.y = y
            sprite = game.selected_sprite(x, y)
            dist_x = 0
            dist_y = 0
            if len(move_array) == 0:
                move_array.append((x, y))
            else:
                move_array.append((x, y))
                dist_x = -(move_array[0][0] - move_array[1][0])
                dist_y = -(move_array[0][1] - move_array[1][1])
                move_array.pop(0)

            if sprite is not None:
                # hier quasi funktion für move
                game.move(sprite, dist_x, dist_y)

            else:
                move_array = []
        # resize or rotate
        if len(sensor.get_value("events")) == 2:
            finger_coordinates = []
            for event_num in range(len(sensor.get_value("events"))):
                sensor_x = float(sensor.get_value("events")[str(event_num)]["x"])
                sensor_y = float(sensor.get_value("events")[str(event_num)]["y"])
                x = int(sensor_x * window.width)
                y = int(window.height - sensor_y * window.height)
                finger_coordinates.append((x, y))

            resize_rotate_array.append(finger_coordinates)
            finger_one.x = finger_coordinates[0][0]
            finger_one.y = finger_coordinates[0][1]
            finger_two.x = finger_coordinates[1][0]
            finger_two.y = finger_coordinates[1][1]
            print(resize_rotate_array)
            if len(resize_rotate_array) == 2:
                finger_coordinates_1 = resize_rotate_array[0]
                finger_coordinates_2 = resize_rotate_array[1]
                # fingercoords für die aktuelle und letzte position
                finger_one_x_1, finger_one_y_1 = finger_coordinates_1[0]
                finger_two_x_1, finger_two_y_1 = finger_coordinates_1[1]
                finger_one_x_2, finger_one_y_2 = finger_coordinates_2[0]
                finger_two_x_2, finger_two_y_2 = finger_coordinates_2[1]
                scale_factor_1 = abs(finger_one_x_1 - finger_two_x_1) / window.width
                scale_factor_2 = abs(finger_one_x_2 - finger_two_x_2) / window.width
                if game.in_image(finger_coordinates_1[0]) and game.in_image(finger_coordinates_2[0]) and game.in_image(finger_coordinates_1[1]) and game.in_image(finger_coordinates_2[1]) is not None:
                    sprite = game.in_image(finger_coordinates_1[0])
                    print("scale FAKTOR: " + str(scale_factor_2)) #abziehen von der eigentlichen scale glaub ich
                    sprite.scale = scale_factor_2
                    resize_rotate_array.pop(0)
                else:
                    resize_rotate_array = []


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
    for i in range(3):
        for point in game.sprite_corners[i]:
            x, y = point
            radius = 10  # Radius des Kreises

            # Kreisfarbe festlegen
            circle_color = (255, 0, 0)  # Rot (RGB-Werte)

            # Kreis zeichnen
            pyglet.shapes.Circle(x, y, radius, color=circle_color).draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.Q:
        sys.exit(0)


# init of DIPPID-sender and touch-detector
touchInput = TouchInput()
clock.schedule_interval(touchInput.touch_input, 0.05)

pyglet.clock.schedule_interval(update, 0.01)
pyglet.app.run()
