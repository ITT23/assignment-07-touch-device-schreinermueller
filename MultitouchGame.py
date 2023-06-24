import os
import pyglet

class MultitouchGame:
    def __init__(self):
        # get all images
        stairsImagePath = os.path.normpath("img/stairs.jpg")
        self.stairsSprite = pyglet.sprite.Sprite(img=pyglet.image.load(stairsImagePath), x=100, y=50)
        self.stairsSprite.scale = 0.3

        tablesImagePath = os.path.normpath("img/tables.jpg")
        self.tablesSprite = pyglet.sprite.Sprite(img=pyglet.image.load(tablesImagePath), x=650, y=30)
        self.tablesSprite.scale = 0.3

        windowsImagePath = os.path.normpath("img/windows.jpg")
        self.windowsSprite = pyglet.sprite.Sprite(img=pyglet.image.load(windowsImagePath), x=300, y=400)
        self.windowsSprite.scale = 0.3

    def draw(self):
        self.stairsSprite.draw()
        self.tablesSprite.draw()
        self.windowsSprite.draw()