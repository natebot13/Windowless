import pyglet, math, json
from pyglet.window import key, mouse
from pyglet.gl import *


class Platform:

    def __init__(self, x1, x2, y1, y2, color=(50, 50, 50, 255)):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.c = color

    def update(self, x1, x2, y1, y2, color=(50, 50, 50, 255)):
        self.__init__(x1, x2, y1, y2, color)


move = [False, False, False, False]
tolerance = 20
offset = [0, 0]
selected = None
gridS = 100
grid = True
window = pyglet.window.Window(resizable=True)
platforms = []
res = [0, 0]
zoom = 1
scroll_speed = 5
for m in pyglet.window.get_platform().get_default_display().get_screens():
    if m.width + abs(m.x) > res[0]:
        res[0] = m.width + abs(m.x)
    if m.height + abs(m.y) > res[1]:
        res[1] = m.height + abs(m.y)


def update_map(map='map'):
    with open(map, 'w') as map:
        Platforms = {'Platforms': [], 'Windows': windows}
        for p in reversed(platforms):
            Platforms['Platforms'].append({'x1': p.x1, 'x2': p.x2, 'y1': p.y1, 'y2': p.y2, 'color': p.c})
        json.dump(Platforms, map)


def read_map(map='map'):
    global windows
    with open(map, 'r') as map:
        map = json.loads(map.read())
        for p in map['Platforms']:
            platforms.append(Platform(p['x1'], p['x2'], p['y1'], p['y2'], tuple(p['color'])))
        windows = map['Windows']


read_map()


def x_to_window(x):
    return round((x - window.get_location()[0] - offset[0] - window.width // 2) * zoom + window.width // 2)


def y_to_window(y):
    return round((window.height // 2 + window.get_location()[1] - y + offset[1]) * zoom + window.height // 2)


def points_to_window(p):
    return [y_to_window(n) if i % 2 else x_to_window(n) for i, n in enumerate(p)]


def x_from_window(x):
    return round((x - window.width / 2) // zoom + window.width / 2 + window.get_location()[0] + offset[0])


def y_from_window(y):
    return round((window.height / 2 - y) // zoom + window.height / 2 + window.get_location()[1] + offset[1])


def points_from_window(p):
    return [y_from_window(n) if i % 2 else x_from_window(n) for i, n in enumerate(p)]


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.S and modifiers == pyglet.window.key.MOD_CTRL:
        update_map()


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
                                         ('v2i', points_to_window([p.x1, p.y2, p.x1, p.y1, p.x2, p.y1, p.x2, p.y2])),
                                         ('c4B', (p.c * 4)))
        if grid:
            y1, y2 = offset[1] + window.get_location()[1] - window.height / 2 // zoom, offset[1] + window.get_location()[1] + window.height / 2 // zoom + window.height
            x1, x2 = offset[0] + window.get_location()[0] - window.width / 2 // zoom, offset[0] + window.get_location()[0] + window.width / 2 // zoom + window.width
            pyglet.gl.glLineWidth(3)
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', points_to_window([x1, 0, x2, 0])))
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', points_to_window([0, y1, 0, y2])))
            pyglet.gl.glLineWidth(1)
            for i in range(math.floor(x1 / gridS) * gridS, math.ceil(x2 / gridS) * gridS, gridS):
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', points_to_window([i, y1, i, y2])))
            for i in range(math.floor(y1 / gridS) * gridS, math.ceil(y2 / gridS) * gridS, gridS):
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', points_to_window([x1, i, x2, i])))


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    dx //= zoom
    dy //= zoom
    if selected:
        x, y = x_from_window(x), y_from_window(y)
        p = platforms[selected[0]]
        if len(selected) == 1:
            p.x1 += dx
            p.x2 += dx
            p.y1 -= dy
            p.y2 -= dy
            return
        if selected[1] == -1:
            if p.x2 < x:
                selected[1] = 1
                p.x1 = p.x2
                p.x2 = x
                return
            p.x1 = x
            if modifiers == pyglet.window.key.MOD_SHIFT:
                p.x1 = round(p.x1 / gridS) * gridS
        elif selected[1] == 1:
            if p.x1 > x:
                selected[1] = -1
                p.x2 = p.x1
                p.x1 = x
                return
            p.x2 = x
            if modifiers == pyglet.window.key.MOD_SHIFT:
                p.x2 = round(p.x2 / gridS) * gridS
        if selected[2] == -1:
            if p.y2 < y:
                selected[2] = 1
                p.y1 = p.y2
                p.y2 = y
                return
            p.y1 = y
            if modifiers == pyglet.window.key.MOD_SHIFT:
                p.y1 = round(p.y1 / gridS) * gridS
        elif selected[2] == 1:
            if p.y1 > y:
                selected[2] = -1
                p.y2 = p.y1
                p.y1 = y
                return
            p.y2 = y
            if modifiers == pyglet.window.key.MOD_SHIFT:
                p.y2 = round(p.y2 / gridS) * gridS
        if selected[1] == -1 and selected[2] == -1:
            window.set_mouse_cursor(window.get_system_mouse_cursor('size_up_left'))
        elif selected[1] == 1 and selected[2] == -1:
            window.set_mouse_cursor(window.get_system_mouse_cursor('size_up_right'))
        elif selected[1] == -1 and selected[2] == 1:
            window.set_mouse_cursor(window.get_system_mouse_cursor('size_down_left'))
        elif selected[1] == 1 and selected[2] == 1:
            window.set_mouse_cursor(window.get_system_mouse_cursor('size_down_right'))
    else:
        window.set_mouse_cursor(window.get_system_mouse_cursor('hand'))
        offset[0] -= dx
        offset[1] += dy


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        global selected
        selected = [0, 0, 0]
        d = False
        x, y = x_from_window(x), y_from_window(y)
        for i, p in enumerate(platforms):
            if p.x1 - tolerance / zoom < x < p.x1 + tolerance / zoom and p.y1 < y < p.y2:
                selected[1] = -1
                window.set_mouse_cursor(window.get_system_mouse_cursor('size_left'))
                d = True
            elif p.x2 - tolerance / zoom < x < p.x2 + tolerance / zoom and p.y1 < y < p.y2:
                selected[1] = 1
                window.set_mouse_cursor(window.get_system_mouse_cursor('size_right'))
                d = True
            if p.y1 - tolerance / zoom < y < p.y1 + tolerance / zoom and p.x1 < x < p.x2:
                selected[2] = -1
                window.set_mouse_cursor(window.get_system_mouse_cursor('size_down'))
                d = True
            elif p.y2 - tolerance / zoom < y < p.y2 + tolerance / zoom and p.x1 < x < p.x2:
                selected[2] = 1
                window.set_mouse_cursor(window.get_system_mouse_cursor('size_up'))
                d = True
            if p.x1 + tolerance / zoom < x < p.x2 - tolerance / zoom and p.y1 + tolerance / zoom < y < p.y2 - tolerance / zoom:
                selected = [i]
                window.set_mouse_cursor(window.get_system_mouse_cursor('hand'))
                return
            if d:
                selected[0] = i
                if selected[1] == -1 and selected[2] == -1:
                    window.set_mouse_cursor(window.get_system_mouse_cursor('size_up_left'))
                elif selected[1] == 1 and selected[2] == -1:
                    window.set_mouse_cursor(window.get_system_mouse_cursor('size_up_right'))
                elif selected[1] == -1 and selected[2] == 1:
                    window.set_mouse_cursor(window.get_system_mouse_cursor('size_down_left'))
                elif selected[1] == 1 and selected[2] == 1:
                    window.set_mouse_cursor(window.get_system_mouse_cursor('size_down_right'))
                return
        else:
            selected = None
    elif button == pyglet.window.mouse.MIDDLE:
        for i, p in enumerate(platforms):
            if p.x1 < x_from_window(x) < p.x2 and p.y1 < y_from_window(y) < p.y2:
                platforms.pop(i)
    elif button == pyglet.window.mouse.RIGHT:
        platforms.append(Platform(x_from_window(x), x_from_window(x), y_from_window(y), y_from_window(y)))
        selected = [len(platforms) - 1, 1, 1]


@window.event
def on_mouse_release(x, y, button, modifiers):
    global selected
    window.set_mouse_cursor(None)
    selected = None


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global zoom
    zoom += scroll_y * zoom * .1


def update(dt):
    if move[0]:
        offset[1] -= scroll_speed
    if move[1]:
        offset[0] -= scroll_speed
    if move[2]:
        offset[1] += scroll_speed
    if move[3]:
        offset[0] += scroll_speed


pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()