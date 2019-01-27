import pyglet, util, math
from typing import Union
from pyglet.window import key
from pyglet.gl import *


class Window(pyglet.window.Window):

    def __init__(self, id: int, effect, fcn: Union[str, None], game, *args, x=0, y=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
        self.set_location(x, y)
        self.x1 = self.get_location()[0]
        self.x2 = self.get_location()[0] + self.width
        self.y1 = self.get_location()[1]
        self.y2 = self.get_location()[1] + self.height
        self.id = id
        self.effect = effect
        self.moving = False
        self.fcn = movements[fcn] if fcn else movements['none']
        self.set_location(x, y)

    def update(self, l: tuple):
        self.move(l[0], l[1])
        self.x1 = self.get_location()[0]
        self.x2 = self.get_location()[0] + self.width
        self.y1 = self.get_location()[1]
        self.y2 = self.get_location()[1] + self.height

    def move(self, x: float, y: float):
        loc = self.fcn(x, y, self, self.game)
        if loc and loc != self.get_location():
            if -self.width < loc[0] < self.game.res[0] and -self.height < loc[1] < self.game.res[1] or self.game.offset == [0, 0]:
                self.set_visible(True)
            else:
                self.set_visible(False)
            self.set_location(round(loc[0]), round(loc[1]))

    def on_draw(self):
        self.clear()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.game.deer.sprite.position = [util.x_to_window(self.game.deer.x,
                                                           self, self.game.offset) - self.game.deer.sprite.width * (self.game.deer.sprite.scale_x-1)/2,
                                          util.y_to_window(self.game.deer.y + self.game.deer.sprite.height * (self.game.deer.sprite.scale_y * .5 - .5),
                                                           self, self.game.offset)]
        self.game.BG.blit(util.x_to_window(0, self, self.game.offset),
                          util.y_to_window(self.game.res[1], self, self.game.offset))
        self.game.deer.sprite.draw()
        for p in self.game.platforms:
            pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 0, 2, 3],
                                         ('v2i', util.points_to_window((p.x1, p.y2, p.x1, p.y1, p.x2, p.y1, p.x2, p.y2),
                                                                       self, self.game.offset)),
                                         ('c4B', ((100, 100, 100, 255) * 4)))

    def on_key_press(self, symbol, modifiers):
        if symbol == key.W or symbol == key.SPACE:
            self.game.deer.jump(self.game.dt)
        if symbol == key.ESCAPE:
            for win in self.game.windows:
                win.close()

    def on_mouse_press(self, x, y, buttons, modifiers): self.moving = True

    def on_mouse_release(self, x, y, button, modifiers): self.moving = False

    def __repr__(self):
        return '%s(width=%d, height=%d, loc=%s)' % \
            (self.__class__.__name__, self.width, self.height, self.get_location())

def follow(w, game):
    x, y = int(game.deer.x - game.offset[0] - (w.width-game.deer.sprite.width)/2),\
           int(game.deer.y - game.offset[1] - w.height/2) + 200
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
    'none': lambda x, y, w, game: w.get_location(),
    'follows': lambda x, y, w, game: follow(w, game),
    'drag': lambda x, y, w, game: (x+game.offset[0], y+game.offset[1]) if w.moving else False,
    'half circle': lambda x, y, w, game: (math.sin((abs(game.time*100 % 360-180)-90)*math.pi/180)*200+4640-game.offset[0],
                                          math.cos((abs(game.time*100 % 360-180)-90)*math.pi/180)*200+400-game.offset[1])
}
