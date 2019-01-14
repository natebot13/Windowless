import json, pyglet
from window import Window
from collision import Platform
from trigger import Trigger


def read_map(game, m: str='map'):
    with open(m, 'r') as m:
        m = json.loads(m.read())
        if 'Platforms' in m:
            game.platforms.clear()
            for t in m['Platforms']:
                game.platforms.append(Platform(t['x1'], t['x2'], t['y1'], t['y2']))
        if 'Triggers' in m:
            game.triggers.clear()
            for t in m['Triggers']:
                game.triggers.append(Trigger(t['x1'], t['x2'], t['y1'], t['y2'],
                                             t['enter'], t['stay'], t['leave'], t['args']))
        if 'Windows' in m:
            for w in game.windows:
                w.close()
            game.windows.clear()
            for i, w in enumerate(m['Windows']):
                w = Window(i+1, w['effect'], w['function'], game, style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS,
                           width=w['width'], height=w['height'])
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
