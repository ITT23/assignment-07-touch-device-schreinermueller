import os
import random

import pyglet
from math import cos, sin, radians


# https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
def point_in_poly(x, y, poly):
    n = len(poly)
    inside = False
    p2x = 0.0
    p2y = 0.0
    xints = 0.0
    p1x, p1y = poly[0]
    for i in range(n+1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

class MultitouchGame:
    def __init__(self):
        # get all images
        self.sprite_corners = []
        stairsImagePath = os.path.normpath("img/stairs.jpg")
        self.stairsSprite = pyglet.sprite.Sprite(img=pyglet.image.load(stairsImagePath), x=300, y=50)
        self.stairsSprite.scale = random.uniform(0.15, 0.5)
        self.stairsSprite.poly = []
        self.stairsSprite.rotation = random.randrange(0, 360, 1)

        tablesImagePath = os.path.normpath("img/tables.jpg")
        self.tablesSprite = pyglet.sprite.Sprite(img=pyglet.image.load(tablesImagePath), x=1000, y=250)
        self.tablesSprite.scale = random.uniform(0.15, 0.5)
        self.stairsSprite.poly = []
        self.tablesSprite.rotation = random.randrange(0, 360, 1)

        windowsImagePath = os.path.normpath("img/windows.jpg")
        self.windowsSprite = pyglet.sprite.Sprite(img=pyglet.image.load(windowsImagePath), x=800, y=400)
        self.windowsSprite.scale = random.uniform(0.15, 0.5)
        self.stairsSprite.poly = []
        self.windowsSprite.rotation = random.randrange(0, 360, 1)

        self.images = [self.stairsSprite, self.windowsSprite, self.tablesSprite]


    def draw(self):
        self.stairsSprite.draw()
        self.tablesSprite.draw()
        self.windowsSprite.draw()

    # check if finger is in an image
    def in_image(self, point):
        x, y = point
        for image in self.images:
            # image.get_transformed_vertices()
            if image.x - 50 <= x <= image.x + 50 + image.width and image.y - 50 <= y <= image.y + 50 + image.height:
                return image
        return None

    def move(self, sprite, dist_x, dist_y):
        sprite.x = sprite.x + dist_x
        sprite.y = sprite.y + dist_y

    def selected_sprite(self, x, y):
        images = [self.stairsSprite, self.tablesSprite, self.windowsSprite]
        for image in images:
            if point_in_poly(x, y, image.poly):
                return image
        return None

    # get all rotated corners
    def get_sprite_corners(self):
        if len(self.sprite_corners) == 3:
            self.sprite_corners = []

        for image in self.images:
            # chatGPT
            # Ursprüngliche Eckpunkte des Sprites
            x1 = image.x
            y1 = image.y
            x2 = x1 + image.width
            y2 = y1
            x3 = x1 + image.width
            y3 = y1 + image.height
            x4 = x1
            y4 = y1 + image.height

            angle = -radians(image.rotation)

            # rotating around upper left corner
            cx = x1
            cy = y1
            # rotated corners
            rotated_x1 = cx + (x1 - cx) * cos(angle) - (y1 - cy) * sin(angle)
            rotated_y1 = cy + (x1 - cx) * sin(angle) + (y1 - cy) * cos(angle)
            rotated_x2 = cx + (x2 - cx) * cos(angle) - (y2 - cy) * sin(angle)
            rotated_y2 = cy + (x2 - cx) * sin(angle) + (y2 - cy) * cos(angle)
            rotated_x3 = cx + (x3 - cx) * cos(angle) - (y3 - cy) * sin(angle)
            rotated_y3 = cy + (x3 - cx) * sin(angle) + (y3 - cy) * cos(angle)
            rotated_x4 = cx + (x4 - cx) * cos(angle) - (y4 - cy) * sin(angle)
            rotated_y4 = cy + (x4 - cx) * sin(angle) + (y4 - cy) * cos(angle)

            image.poly = [(rotated_x1, rotated_y1), (rotated_x2, rotated_y2), (rotated_x3, rotated_y3),
                          (rotated_x4, rotated_y4)]
            self.sprite_corners.append([(rotated_x1, rotated_y1), (rotated_x2, rotated_y2), (rotated_x3, rotated_y3),
                                        (rotated_x4, rotated_y4)])

