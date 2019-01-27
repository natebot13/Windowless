import pyglet
from collision import Platform
from window import Window


class Trigger(Platform):
    def __init__(self, x1: float, x2: float, y1: float, y2: float, enter: str, stay: str, leave: str, args: tuple):
        super().__init__(x1, x2, y1, y2)
        self.args = args
        self.active = False
        self.enter = triggers[enter] if enter else triggers['none']
        self.stay = triggers[stay] if stay else triggers['none']
        self.leave = triggers[leave] if leave else triggers['none']


def trigger_check(game):
    for trigger in game.triggers:
        if trigger.collide(game.deer.x, game.deer.y, game.deer.sprite.width, game.deer.sprite.height):
            if trigger.active:
                trigger.stay(trigger, trigger.args[1], trigger.args[3], game)
            else:
                trigger.enter(trigger, trigger.args[0], trigger.args[3], game)
            trigger.active = True
        elif trigger.active:
            trigger.leave(trigger, trigger.args[2], trigger.args[3], game)
            trigger.active = False


def open_window(trigger: Trigger, p, g, game):
    if g['window'] == -1:
        game.windows.append(Window(len(game.windows), None, None, game,
                                   style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS,
                                   x=p['x']-game.offset[0], y=p['y']-game.offset[1], width=p['width'], height=p['height']))
        g['window'] = len(game.windows) - 1


def close_window(trigger: Trigger, p, g, game):
    if not g['window'] == -1:
        game.windows.sort(key=lambda val: val.id)
        game.windows[g['window']].close()
        game.windows.pop(g['window'])
        g['window'] = -1


triggers = {
    'none': lambda trigger, p, g, game: None,
    'win open': open_window,
    'win close': close_window,
    'ech': lambda trigger, p, g, game: print(game.windows)
}


