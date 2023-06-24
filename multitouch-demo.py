# task 2
import pyglet
import sys
from MultitouchGame import MultitouchGame

# fullscreen window
window = pyglet.window.Window(fullscreen=True)

game = MultitouchGame()

@window.event
def on_draw():
    window.clear()
    game.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.Q:
        sys.exit(0)


pyglet.app.run()
