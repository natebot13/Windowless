import pyglet, util, math
from typing import Union
from pyglet.window import key
from pyglet.gl import *
from effects import effects
from trigger import Trigger


class Window(pyglet.window.Window):
    def __init__(self, name: str, effect, fcn: Union[str, None], game, *args, visible=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
        self.set_visible(visible)
        self.set_caption(name)
        self.set_location(0, 0)
        self.x1 = self.get_location()[0]
        self.x2 = self.get_location()[0] + self.width
        self.y1 = self.get_location()[1]
        self.y2 = self.get_location()[1] + self.height
        self.name = name
        self.effect, self.color = effects[effect]
        self.trigger = Trigger(self.x1, self.x2, self.y1, self.y2,
                               enter=('effect', {'effect': self.effect, 'apply': True}),
                               leave=('effect', {'effect': self.effect, 'apply': False}))

        if effect != 'none': self.game.triggers.append(self.trigger)
        self.moving = False
        self.on_close = lambda: None
        self.fcn = lambda game: movements[fcn[0]](game, **fcn[1]) if fcn[0] else movements['static'](game)

    def update(self):
        self.push_handlers(self.game.keys)
        self.move()
        self.x1, self.x2 = self.get_location()[0], self.get_location()[0] + self.width
        self.y1, self.y2 = self.get_location()[1],self.get_location()[1] + self.height
        self.trigger.x1, self.trigger.x2, self.trigger.y1, self.trigger.y2 = self.x1, self.x2, self.y1, self.y2

    def move(self):
        loc = self.fcn(self.game)
        loc = round(loc[0]), round(loc[1])
        if loc and loc != self.get_location():
            if -self.width < loc[0] < self.game.res[0] and -self.height < loc[1] < self.game.res[1]:
                self.set_visible(True)
            else:
                self.set_visible(False)
            self.set_location(loc[0], loc[1])

    def on_draw(self):
        self.clear()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.game.deer.sprite.position = [util.x_to_window(self.game.deer.x, self, self.game.offset)
                                          - self.game.deer.sprite.width
                                          * (self.game.deer.sprite.scale_x-1)/2,
                                          util.y_to_window(self.game.deer.y + self.game.deer.sprite.height
                                                           * (self.game.deer.sprite.scale_y * .5 - .5)
                                                           , self, self.game.offset)]
        self.game.BG.blit(util.x_to_window(0, self, self.game.offset),
                          util.y_to_window(self.game.res[1], self, self.game.offset))
        self.game.deer.sprite.draw()
        for p in self.game.platforms:
            pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 0, 2, 3],
                                         ('v2i', util.points_to_window((p.x1, p.y2, p.x1, p.y1, p.x2, p.y1, p.x2, p.y2),
                                                                       self, self.game.offset)),
                                         ('c4B', ((100, 100, 100, 255) * 4)))
        for w in self.game.windows.values():
            pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 0, 2, 3],
                                         ('v2i', util.points_to_window((w.x1, w.y2, w.x1, w.y1, w.x2, w.y1, w.x2, w.y2),
                                                                       self, [0, 0])),
                                         ('c4B', (w.color * 4)))
        self.update()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.W or symbol == key.SPACE:
            self.game.deer.jump(self.game.dt)
        if symbol == key.ESCAPE:
            self.game.close()

    def __repr__(self):
        return '%s(width=%d, height=%d, loc=%s)' % \
            (self.__class__.__name__, self.width, self.height, self.get_location())


def follow(game, w):
    w = game.windows[w]
    x, y = int(game.deer.x - game.offset[0] - (w.width-game.deer.sprite.width)/2),\
           int(game.deer.y - game.offset[1] - w.height/2)
    if w.width / 2 > game.deer.x - game.offset[0]:
        x = 0
    if game.deer.x - game.offset[0] > game.res[0] - (w.width / 2):
        x = game.res[0] - w.width
    if w.height / 2 > game.deer.y - game.offset[1]:
        y = 0
    if game.deer.y - game.offset[1] > game.res[1] - (w.height / 2):
        y = game.res[1] - w.height
    return x, y



movements = {
    'static': lambda game, x=0, y=0: (util.x_to_pixels(game, x)-game.offset[0], util.y_to_pixels(game, y)-game.offset[1]),
    'follows': lambda game, name='main': follow(game, name),
    'half circle': lambda game, x=0, y=0, size=200, speed=100: (math.sin((abs(game.time*speed % 360-180)-90)*math.pi/180)*size+util.x_to_pixels(game, x)-game.offset[0],
                                                                math.cos((abs(game.time*speed % 360-180)-90)*math.pi/180)*size+util.y_to_pixels(game, y)-game.offset[1])
}
