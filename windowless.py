import pyglet, math
from screeninfo import get_monitors
from random import randint
from pyglet.window import key, mouse
from pyglet.gl import *

"""
    Notes:
        * Window Location measured form top left of screen to top left of window
            * same for platforms and player
        * Rendering form bottom left of window
"""


class Platform:

    def __init__(self, x1, x2, y, h):
        self.x1 = x1
        self.x2 = x2
        self.y = y
        self.h = h

    def update(self, x1, x2, y, h):
        self.__init__(x1, x2, y, h)


class Deer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xSpeed = 0
        self.ySpeed = 0
        self.frame = 10
        self.seq = pyglet.image.ImageGrid(pyglet.resource.image('deer.png'), 5, 5)
        self.sprite = pyglet.sprite.Sprite(img=self.seq[self.frame])

    def jump(self):
        self.ySpeed = -7

    def update(self):
        if abs(self.xSpeed) + abs(self.ySpeed) < .1:
            self.frame = 20 if self.frame >= 24 else self.frame + .3
        else:
            self.frame = 10 if self.frame >= 14 else self.frame + .05 + math.sqrt(abs(self.xSpeed / 50))
        self.sprite.image = self.seq[round(self.frame)]
        self.x, self.y = self.x + self.xSpeed, self.y + self.ySpeed
        self.xSpeed, self.ySpeed = self.xSpeed / 1.1, self.ySpeed + .2 / 1.1
        for p in platforms: #+ window_platforms:
            if self.ySpeed > 0 and p.x1 - deer.sprite.width/2 < self.x < p.x2 + deer.sprite.width/2 and p.y + p.h > self.y >= p.y:
                self.ySpeed = 0
                self.y = p.y
        if keys[key.A]:
            self.sprite.scale_x = -1
            self.xSpeed -= 1
        elif keys[key.D]:
            self.sprite.scale_x = 1
            self.xSpeed += 1
        if res[0] + offset[0] < self.x < offset[0] and res[1] + offset[1] < self.y < offset[1]:
            scroll()


deer = Deer(10, 0)
BG = pyglet.image.load("BG.png")
keys = key.KeyStateHandler()
windows = []
for i in range(3):
    windows.append(pyglet.window.Window(style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS))
res = [0, 0]
for m in pyglet.window.get_platform().get_default_display().get_screens():
    if m.width + abs(m.x) > res[0]:
        res[0] = m.width + abs(m.x)
    if m.height + abs(m.y) > res[1]:
        res[1] = m.height + abs(m.y)
offset = [0, 0]
move = [0, 0]
platforms = [Platform(100, 200, 200, 200)]
#window_platforms = []
mouseLoc = [0, 0]
moving = False
label1 = pyglet.text.Label('Window1', font_name='Times New Roman', font_size=36, x=windows[0].width//2, y=windows[0].height//2
                           , anchor_x='center', anchor_y='center')
label2 = pyglet.text.Label('Window2', font_name='Times New Roman', font_size=36, x=windows[1].width//2, y=windows[1].height//2
                           , anchor_x='center', anchor_y='center')

def scroll():
    offset = [0, 0]


def x_to_window(x, w):
    return x - w.get_location()[0]


def y_to_window(y, w):
    return w.get_size()[1] + w.get_location()[1] - y


def points_to_window(p, w):
    return [y_to_window(n, w) if i % 2 else x_to_window(n, w) for i, n in enumerate(p)]


def x_from_window(x, w):
    return x + w.get_location()[0]


def y_from_window(y, w):
    return w.get_size()[1] - y + w.get_location()[1]


def points_from_window(p, w):
    return [y_from_window(n, w) if i % 2 else x_from_window(n, w) for i, n in enumerate(p)]


# def make_window_platforms():
#     global window_platforms
#     window_platforms = []
#     windows.sort(key=lambda x: x.get_location()[0])
#     for w in windows:
#         p = Platform(w.get_location()[0], w.get_location()[0] + w.width, w.get_location()[1] + w.height, 20)
#         for o in windows:
#             if o.get_location()[1] + o.height > w.get_location()[1] + w.height > o.get_location()[1] and o.get_location()[0] + o.height > w.get_location()[0]:
#                 window_platforms.append(Platform(p.x1, o.get_location()[0], p.y, 20))
#                 p.x1 = o.get_location()[0] + o.width
#                 if p.x1 > p.x2:
#                     break
#         else:
#             window_platforms.append(p)


def on_draw(w, i):
    def helper():
        w.clear()
        glEnable(GL_BLEND)
        label1.draw()
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        if not i:
            deer.sprite.position = [w.width/2 + deer.sprite.width * -.5 * deer.sprite.scale_x, w.height/2]
            w.set_location(int(deer.x-w.width/2), int(deer.y-w.height/2))
        else:
            deer.sprite.position = [x_to_window(deer.x, w) + deer.sprite.width * -.5 * deer.sprite.scale_x - offset[0], y_to_window(deer.y, w) - offset[1]]
        BG.blit(x_to_window(0, w) - offset[0], y_to_window(res[1], w) - offset[1])
        deer.sprite.draw()
        for p in platforms:
            pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 0, 2, 3],
                                         ('v2i', points_to_window([p.x1, p.y + p.h, p.x1, p.y, p.x2, p.y, p.x2, p.y + p.h], w)),
                                         ('c3B', (0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255 )))
    return helper


def on_key_press(w, i):
    def helper(symbol, modifiers):
        if symbol == key.W or symbol == key.SPACE:
            deer.jump()
        if symbol == key.ESCAPE:
            w.close()
    return helper


def on_mouse_drag(w, i):
    def helper(x, y, dx, dy, buttons, modifiers):
        global moving, mouseLoc
        if not moving:
            moving = True
            mouseLoc = x, y
        if buttons & mouse.LEFT:
            x, y = x - mouseLoc[0], y - mouseLoc[1]
            if x + y != 0:
                xs, ys = w.get_location()
                w.set_location(xs + x, ys - y)
                #make_window_platforms()
    return helper


def on_mouse_release(w, i):
    def helper(x, y, button, modifiers):
        global moving
        moving = False
    return helper


for i, w in enumerate(windows):
    w.on_key_press = on_key_press(w, i)
    w.on_draw = on_draw(w, i)
    w.on_mouse_drag = on_mouse_drag(w, i)
    w.on_mouse_release = on_mouse_release(w, i)


def update(dt):
    for w in windows:
        w.push_handlers(keys)
    deer.update()


#make_window_platforms()
pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()
