import esper, util, pyglet, trigger
from deer import Deer, effects, processors
from window import Window
from trigger import Trigger
from collision import Platform
from pyglet.window import key, mouse


class Game:
    def __init__(self):
        self.deer = Deer(3000, 0)
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
            self.res[0] = self.res[1] * 16 / 9
        elif self.res[0] / self.res[1] < 16 / 9:
            self.res[1] = self.res[0] * 9 / 16
        self.mouseLoc = [0, 0]
        for m in pyglet.window.get_platform().get_default_display().get_screens():
            if m.width + abs(m.x) > self.res[0]:
                self.res[0] = m.width + abs(m.x)
            if m.height + abs(m.y) > self.res[1]:
                self.res[1] = m.height + abs(m.y)
        self.windows = [Window(0, None, None, self, style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)]
        self.keys = key.KeyStateHandler()
        self.world = esper.World()
        self.deer.id = self.world.create_entity(self.deer)
        util.read_map(self)
        for processor in processors:
            self.world.add_processor(processor())
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

    def update(self, dt):
        if dt > .1:
            return
        self.time += dt
        self.dt = dt
        for w in self.windows:
            w.update(util.points_from_window((w._mouse_x - self.mouseLoc[0] - self.offset[0],
                                              w._mouse_y - self.mouseLoc[1] - self.offset[1]), w, self.offset))
            w.push_handlers(self.keys)
        self.world.process(dt)
        self.deer.update(game)
        trigger.trigger_check(game)




game = Game()

pyglet.app.run()
