import pyglet, math, json
from pyglet.window import key, mouse
from pyglet.gl import *


class Platform:

    def __init__(self, x1, x2, y, h, color=(0, 0, 0, 255)):
        self.x1 = x1
        self.x2 = x2
        self.y = y
        self.h = h
        self.c = color

    def update(self, x1, x2, y, h, color=(0, 0, 0, 255)):
        self.__init__(x1, x2, y, h, color)


move = [False, False, False, False]
offset = [0, 0]
selected = None
gridS = 100
grid = False
window = pyglet.window.Window(resizable=True)
platforms = [Platform(0, 100, 0, 100, (50, 50, 50, 255))]
res = [0, 0]
for m in pyglet.window.get_platform().get_default_display().get_screens():
    if m.width + abs(m.x) > res[0]:
        res[0] = m.width + abs(m.x)
    if m.height + abs(m.y) > res[1]:
        res[1] = m.height + abs(m.y)


def update_map(map='map'):
    with open(map, 'w') as map:
        Platforms = {}
        Platforms['Platforms'] =[]
        for p in platforms:
            Platforms['Platforms'].append({'x1': p.x1, 'x2': p.x2, 'y': p.y, 'h': p.h, 'color': p.c})
        json.dump(Platforms, map)


def x_to_window(x):
    return x - window.get_location()[0] - offset[0]


def y_to_window(y):
    return window.get_size()[1] + window.get_location()[1] - y + offset[1]


def points_to_window(p):
    return [y_to_window(n) if i % 2 else x_to_window(n) for i, n in enumerate(p)]


def x_from_window(x):
    return x + window.get_location()[0] + offset[0]


def y_from_window(y):
    return -window.get_size()[1] - window.get_location()[1] + y - offset[1]


def points_from_window(p):
    return [y_from_window(n) if i % 2 else x_from_window(n) for i, n in enumerate(p)]


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.W or symbol == key.UP:
        move[0] = True
    if symbol == key.A or symbol == key.LEFT:
        move[1] = True
    if symbol == key.S or symbol == key.DOWN:
        move[2] = True
    if symbol == key.D or symbol == key.RIGHT:
        move[3] = True


@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.W or symbol == key.UP:
        move[0] = False
    if symbol == key.A or symbol == key.LEFT:
        move[1] = False
    if symbol == key.S or symbol == key.DOWN:
        move[2] = False
    if symbol == key.D or symbol == key.RIGHT:
        move[3] = False


@window.event
def on_draw():
        window.clear()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        for p in platforms:
            pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 0, 2, 3],
                                         ('v2i', points_to_window([p.x1, p.y + p.h, p.x1, p.y, p.x2, p.y, p.x2, p.y + p.h])),
                                         ('c4B', (p.c * 4)))
        if grid:
            pyglet.gl.glLineWidth(3)
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', points_to_window([10000000, 0, -1000000, 0])))
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', points_to_window([0, 10000000, 0, -1000000])))
            pyglet.gl.glLineWidth(1)
            for i in range(math.ceil(offset[0] / gridS) * gridS, math.ceil(offset[0] / gridS) * gridS + window.width + window.get_location()[0], gridS):
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', points_to_window([i, 10000000, i, -1000000])))
            for i in range(math.ceil(offset[1] / gridS) * gridS, math.ceil(offset[1] / gridS) * gridS + window.height + window.get_location()[1], gridS):
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', points_to_window([1000000, i, -1000000, i])))


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    print(selected)
    if selected:
        x, y = x_from_window(x), -y_from_window(y)
        p = platforms[selected[0]]
        if selected[1] == 0 or selected[1] == 1:
            if p.h + p.y < y:
                selected[1] += 2
                p.y += p.h
                p.h = y - p.y
                return
            p.y = y
            p.h += dy
        elif selected[1] == 2 or selected[1] == 3:
            if p.y > y:
                selected[1] -= 2
                p.h = p.y - y
                p.y = y
                return
            p.h = y - p.y
        if selected[1] == 0 or selected[1] == 2:
            if p.x2 < x:
                selected[1] += 1
                p.x1 = p.x2
                p.x2 = x
                return
            p.x1 = x
        elif selected[1] == 1 or selected[1] == 3:
            if p.x1 > x:
                selected[1] -= 1
                p.x2 = p.x1
                p.x1 = x
                return
            p.x2 = x
    else:
        offset[0] -= dx
        offset[1] += dy



@window.event
def on_mouse_press(x, y, button, modifiers):
    global selected
    for i, p in enumerate(platforms):
        if p.x1 - 10 < x_from_window(x) < p.x1 + 10 and p.y - 10 < -y_from_window(y) < p.y + 10:
            selected = [i, 0]
            break
        elif p.x2 - 10 < x_from_window(x) < p.x2 + 10 and p.y - 10 < -y_from_window(y) < p.y + 10:
            selected = [i, 1]
            break
        elif p.x1 - 10 < x_from_window(x) < p.x1 + 10 and p.y + p.h - 10 < -y_from_window(y) < p.y + p.h + 10:
            selected = [i, 2]
            break
        elif p.x2 - 10 < x_from_window(x) < p.x2 + 10 and p.y + p.h - 10 < -y_from_window(y) < p.y + p.h + 10:
            selected = [i, 3]
            break


@window.event
def on_mouse_release(x, y, button, modifiers):
    global selected
    selected = None


def update(dt):
    speed = 5
    if move[0]:
        offset[1] -= speed
    if move[1]:
        offset[0] -= speed
    if move[2]:
        offset[1] += speed
    if move[3]:
        offset[0] += speed


update_map()

pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()