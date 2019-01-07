import pyglet, math, esper
from pyglet.window import key


class Deer:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.grounded = False
        self.xSpeed = 0
        self.ySpeed = 0
        self.frame = 10
        self.gravity = 1
        self.jumpStrength = 25
        self.id = None
        self.seq = pyglet.image.ImageGrid(pyglet.resource.image('deer.png'), 5, 5)
        self.sprite = pyglet.sprite.Sprite(img=self.seq[self.frame])

    def jump(self):
        if self.grounded:
            self.ySpeed -= self.jumpStrength

    def update(self, game):
        if abs(self.xSpeed) + abs(self.ySpeed) < .1: self.frame = 20 if self.frame >= 24 else self.frame + .3
        else: self.frame = 10 if self.frame >= 14 else self.frame + .05 + math.sqrt(abs(self.xSpeed / 50))
        self.sprite.image = self.seq[round(self.frame)]
        self.xSpeed, self.ySpeed = self.xSpeed / 1.06, (self.ySpeed + self.gravity) / 1.06
        self.grounded = False
        for p in game.platforms:
            if p.collide(self.x + self.xSpeed, self.y + self.ySpeed, self.sprite.width, self.sprite.height):
                if not p.collide_x(self.x, self.sprite.width):
                    if self.xSpeed > 0:
                        self.xSpeed = p.x1 - self.sprite.width - self.x
                    else:
                        self.xSpeed = p.x2 - self.x
                if not p.collide_y(self.y, self.sprite.height):
                    if self.ySpeed < 0:
                        self.ySpeed = p.y2 + self.sprite.height - self.y
                    else:
                        self.grounded = True
                        self.ySpeed = p.y1 - self.y
        self.x, self.y = self.x + self.xSpeed, self.y + self.ySpeed
        if game.world.has_component(self.id, effects["AGC"]):
            self.sprite.scale_y = 1
            game.world.remove_component(self.id, effects["AGC"])
        if game.world.has_component(self.id, effects["WC"]):
            game.world.remove_component(self.id, effects["WC"])
        for w in game.windows:
            if w.x1 - self.sprite.width < self.x - game.offset[0] < w.x2 and w.y2 + self.sprite.height > self.y - game.offset[1] > w.y1 and w.effect:
                game.world.add_component(self.id, effects[w.effect]() if effects[w.effect] else effects['none'])
        if game.keys[key.A]:
            self.sprite.scale_x = -1
            self.xSpeed -= .8
        elif game.keys[key.D]:
            self.sprite.scale_x = 1
            self.xSpeed += .8
        if game.res[0] + game.offset[0] < self.x:
            game.offset[0] += game.res[0]
        if self.x < game.offset[0]:
            game.offset[0] -= game.res[0]
        if game.res[1] + game.offset[1] < self.y:
            game.offset[1] += game.res[1]
        if self.y < game.offset[1]:
            game.offset[1] -= game.res[1]


class DPC:
    pass


class DPS(esper.Processor):
    def process(self, dt):
        pass


class AGC:
    pass


class AGS(esper.Processor):
    def process(self, dt):
        for ent, (deer, agc) in self.world.get_components(Deer, AGC):
            deer.ySpeed = (deer.ySpeed * 1.06 - deer.gravity * 2) / 1.06
            deer.sprite.scale_y = -1


class WC:
    pass


class WS(esper.Processor):
    def process(self, dt):
        for ent, (deer, wc) in self.world.get_components(Deer, WC):
            deer.xSpeed = deer.xSpeed * 1.05
            deer.ySpeed = deer.ySpeed * 1.05


processors = (DPS, AGS, WS)

effects = {
    'none': DPC,
    'AGC': AGC,
    'WC': WC
}
