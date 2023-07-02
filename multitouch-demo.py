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
    print("data")


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
            if len(resize_rotate_array) == 2:
                finger_coordinates_1 = resize_rotate_array[0]
                finger_coordinates_2 = resize_rotate_array[1]
                # fingercoords für die aktuelle und letzte position
                finger_one_x_1, finger_one_y_1 = finger_coordinates_1[0]
                finger_two_x_1, finger_two_y_1 = finger_coordinates_1[1]
                finger_one_x_2, finger_one_y_2 = finger_coordinates_2[0]
                finger_two_x_2, finger_two_y_2 = finger_coordinates_2[1]
                

                dist_x_1 = abs(finger_one_x_1 - finger_two_x_1) / window.width
                dist_x_2 = abs(finger_one_x_2 - finger_two_x_2) / window.width
                dist_y_1 = abs(finger_one_y_1 - finger_two_y_1) / window.width
                dist_y_2 = abs(finger_one_y_2 - finger_two_y_2) / window.width


                # resize
                if dist_x_2 - dist_x_1 > 100:
                    if game.in_image(finger_coordinates_1[0]) and game.in_image(finger_coordinates_2[0]) and game.in_image(finger_coordinates_1[1]) and game.in_image(finger_coordinates_2[1]) is not None:
                        sprite = game.in_image(finger_coordinates_1[0])
                        if not sprite is None:
                            sprite.scale += 0.2
                            resize_rotate_array.pop(0)
                            print("RESIZE")
                elif dist_x_1 - dist_x_2 > 100:
                    if game.in_image(finger_coordinates_1[0]) and game.in_image(finger_coordinates_2[0]) and game.in_image(finger_coordinates_1[1]) and game.in_image(finger_coordinates_2[1]) is not None:
                        sprite = game.in_image(finger_coordinates_1[0])
                        if not sprite is None:
                            sprite.scale -= 0.2
                            resize_rotate_array.pop(0)
                            print("LARGER")

                # rotate
                bottom_right = False
                bottom_left = False
                upper_left = False
                upper_right = False
                delta = 200

                for i in range(3):
                    for point in game.sprite_corners[i]:
                        x, y = point
                        dist_finger_1 = x - delta <= finger_one_x_1 <= x + delta and y - delta <= finger_one_y_1 <= y + delta
                        dist_finger_2 = x - delta <= finger_two_x_1 <= x + delta and y - delta <= finger_two_y_1 <= y + delta
                        print(dist_finger_1, dist_finger_2)
                        # bottom left corner
                        if i == 0:
                            if dist_finger_1 or dist_finger_2:
                                print("bottom left")
                                bottom_left = True

                        elif i == 1:
                            if dist_finger_1 or dist_finger_2:
                                bottom_right = True
                                print("bottom right")

                        elif i == 2 and bottom_left:
                            if dist_finger_1 or dist_finger_2:
                                upper_right = True

                        elif i == 3 and bottom_right:
                            if dist_finger_1 or dist_finger_2:
                                upper_left = True

                if upper_right:
                    print("upper right")
                    if game.in_image(finger_coordinates_1[0]) and game.in_image(finger_coordinates_2[0]) and game.in_image(finger_coordinates_1[1]) and game.in_image(finger_coordinates_2[1]) is not None:
                        sprite = game.in_image(finger_coordinates_1[0])
                        if not sprite is None:
                            sprite.rotation += 3
                            resize_rotate_array.pop(0)
                elif upper_left:
                    print("upper left")
                    if game.in_image(finger_coordinates_1[0]) and game.in_image(finger_coordinates_2[0]) and game.in_image(finger_coordinates_1[1]) and game.in_image(finger_coordinates_2[1]) is not None:
                        sprite = game.in_image(finger_coordinates_1[0])
                        if not sprite is None:
                            sprite.rotation -= 3
                            resize_rotate_array.pop(0)
                else:
                    print("else")
                    resize_rotate_array = []



                # wenn die x veränderung > als y veränderung dann resize (bin mir nicht sicher ob das als constraint gut ist)
                # if dist_x_1+dist_x_2 > dist_y_1+dist_y_2:
                #     if game.in_image(finger_coordinates_1[0]) and game.in_image(finger_coordinates_2[0]) and game.in_image(finger_coordinates_1[1]) and game.in_image(finger_coordinates_2[1]) is not None:
                #         sprite = game.in_image(finger_coordinates_1[0])
                #         sprite.scale -= 0.2
                #         resize_rotate_array.pop(0)
                #     else:
                #         resize_rotate_array = []
                # # wenn die x veränderung < als y veränderung dann rotate
                # else:
                #     if game.in_image(finger_coordinates_1[0]) and game.in_image(finger_coordinates_2[0]) and game.in_image(finger_coordinates_1[1]) and game.in_image(finger_coordinates_2[1]) is not None:
                #         sprite = game.in_image(finger_coordinates_1[0])
                #         sprite.rotation += 3
                #         resize_rotate_array.pop(0)
                #     else:
                #         resize_rotate_array = []


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
