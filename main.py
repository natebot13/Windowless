import util, pyglet, trigger
from deer import Deer
from window import Window
from trigger import Trigger
from collision import Platform
from pyglet.window import key, mouse


class Game:
    def __init__(self):
        self.BG = pyglet.image.load('bg.png')
        self.time = 0
        self.dt = 0
        self.platforms = []
        self.triggers = []
        self.offset = [0, 0]
        self.move = [0, 0]
        self.res = [pyglet.window.get_platform().get_default_display().get_default_screen().width,
                    pyglet.window.get_platform().get_default_display().get_default_screen().height]
        if self.res[0] / self.res[1] > 16 / 9:
            self.res[0] = round(self.res[1] * 16 / 9)
        elif self.res[0] / self.res[1] < 16 / 9:
            self.res[1] = round(self.res[0] * 9 / 16)
        self.mouseLoc = [0, 0]
        self.objects = [Deer(self, 1.5, 0)]
        self.deer = self.objects[0]
        self.windows = {}
        self.keys = key.KeyStateHandler()
        util.read_map(self)
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

    def close(self):
        for w in self.windows.values():
            w.close()

    def update(self, dt):
        if dt > .1:
            return
        self.time += dt
        self.dt = dt
        self.deer.update()
        trigger.trigger_check(game)




game = Game()

pyglet.app.run()
