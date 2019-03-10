import pyglet
from collision import Platform


class Trigger(Platform):
    def __init__(self, x1: float, x2: float, y1: float, y2: float,
                 enter: list = ['none', {}], stay: list = ['none', {}], leave: list = ['none', {}]):
        super().__init__(x1, x2, y1, y2)
        self.active = False
        self.enter = lambda game, obj: triggers[enter[0]](game, obj, **enter[1])
        self.stay = lambda game, obj: triggers[stay[0]](game, obj, **stay[1])
        self.leave = lambda game, obj: triggers[leave[0]](game, obj, **leave[1])


def trigger_check(game):
    for obj in game.objects:
        for trigger in game.triggers:
            if trigger.collide(obj.x, obj.y, obj.sprite.width, obj.sprite.height):
                if trigger.active:
                    trigger.stay(game, obj)
                else:
                    print(trigger.x1, trigger.x2, trigger.y1)
                    trigger.enter(game, obj)
                trigger.active = True
            elif trigger.active:
                trigger.leave(game, obj)
                trigger.active = False


def open_window(game, obj, window: str = 'main'):
    if window in game.windows:
        game.windows[window].set_visible(True)
    else: raise Exception("Invalid args")


def close_window(game, obj, window: str = 'main'):
    if window in game.windows:
        game.windows[window].set_visible(False)
    else: raise Exception("Invalid args")


triggers = {
    'none': lambda game, obj: None,
    'effect': lambda game, obj, effect, apply: (effect(game, obj, apply), print(apply)),
    'win open': open_window,
    'win close': close_window,
}


