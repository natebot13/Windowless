import json, pyglet
from window import Window
from collision import Platform

def read_map(game, m:str='map'):
    with open(m, 'r') as m:
        m = json.loads(m.read())
        game.platforms.clear()
        for p in m['Platforms']:
            game.platforms.append(Platform(p['x1'], p['x2'], p['y1'], p['y2'], tuple(p['color'])))
        for w in game.windows:
            w.close()
        game.windows.clear()
        for i, w in enumerate(m['Windows']):
            w = Window(i+1, w['effect'], w['function'], game, style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS, width=w['width'], height=w['height'])
            game.windows.append(w)


def x_to_window(x: int, w: Window, offset):
    return x - w.x1 - offset[0]


def y_to_window(y: int, w: Window, offset):
    return w.y2 - y + offset[1]


def points_to_window(p: tuple, w: Window, offset):
    return [y_to_window(n, w, offset) if i % 2 else x_to_window(n, w, offset) for i, n in enumerate(p)]


def x_from_window(x: int, w: Window, offset):
    return x + w.x1 + offset[0]


def y_from_window(y: int, w: Window, offset):
    return w.y2 - y + offset[1]


def points_from_window(p: tuple, w: Window, offset):
    return [y_from_window(n, w, offset) if i % 2 else x_from_window(n, w, offset) for i, n in enumerate(p)]
