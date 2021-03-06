import json, pyglet
from window import Window
from collision import Platform
from trigger import Trigger


def x_to_pixels(game, *x):
    return [round(game.res[0] * i) for i in x] if len(x) > 1 else round(game.res[0] * x[0])


def y_to_pixels(game, *y):
    return [round(game.res[1] * i) for i in y] if len(y) > 1 else round(game.res[1] * y[0])


def read_map(game, m: str='map'):
    with open(m, 'r') as m:
        m = json.loads(m.read())
        if 'Start' in m:
            game.start = m['Start']
        if 'Platforms' in m:
            game.platforms.clear()
            for p in m['Platforms']:
                game.platforms.append(Platform(*x_to_pixels(game, p['x1'], p['x2']),
                                               *y_to_pixels(game, p['y1'], p['y2'])))
        if 'Triggers' in m:
            game.triggers.clear()
            for t in m['Triggers']:
                game.triggers.append(Trigger(*x_to_pixels(game, t['x1'], t['x2']),
                                      *y_to_pixels(game, t['y1'], t['y2']),
                                      t['enter'], t['stay'], t['leave']))
        if 'Windows' in m:
            for w in game.windows.values():
                w.close()
            game.windows = {}
            for w in m['Windows']:
                win = Window(w['name'], w['effect'], w['function'], game,
                             style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS,
                             width=x_to_pixels(game, w['width']), height=y_to_pixels(game, w['height']),
                             visible=w['visible'])
                game.windows[w['name']] = win


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
