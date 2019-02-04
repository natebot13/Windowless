import pyglet, math, esper
from pyglet.window import key


class Deer:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.grounded = 0
        self.xSpeed = 0.0
        self.ySpeed = 0.0
        self.frame = 10
        self.drag = 1.06
        self.gravity = 1500.0
        self.speed = 1500.0
        self.jumpStrength = 1500.0
        self.id = None
        self.seq = pyglet.image.ImageGrid(pyglet.resource.image('deer.png'), 5, 5)
        self.sprite = pyglet.sprite.Sprite(img=self.seq[self.frame])

    def jump(self, dt):
        if self.grounded > 0:
            self.ySpeed -= self.jumpStrength
            self.grounded = 0

    def collision_check(self, game):
        self.xSpeed, self.ySpeed = self.xSpeed * game.dt, self.ySpeed * game.dt
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
                        self.grounded = .08
                        self.ySpeed = p.y1 - self.y
        self.xSpeed, self.ySpeed = self.xSpeed / game.dt, self.ySpeed / game.dt

    def window_check(self, game):
        if game.world.has_component(self.id, effects["AGC"]):
            self.sprite.scale_y = 1
            self.gravity = abs(self.gravity)
            game.world.remove_component(self.id, effects["AGC"])
        if game.world.has_component(self.id, effects["WC"]):
            game.world.remove_component(self.id, effects["WC"])
        for w in game.windows:
            if w.x1 - self.sprite.width < self.x - game.offset[0] < w.x2 \
                    and w.y2 + self.sprite.height > self.y - game.offset[1] > w.y1 and w.effect:
                game.world.add_component(self.id, effects[w.effect]() if effects[w.effect] else effects['none'])

    def scroll_check(self, game):
        if game.res[0] + game.offset[0] < self.x:
            game.offset[0] += game.res[0]
        if self.x < game.offset[0]:
            game.offset[0] -= game.res[0]
        if game.res[1] + game.offset[1] < self.y:
            game.offset[1] += game.res[1]
        if self.y < game.offset[1]:
            game.offset[1] -= game.res[1]

    def update(self, game):
        if game.keys[key.A]:
            self.sprite.scale_x = -1
            self.xSpeed -= self.speed * game.dt
        elif game.keys[key.D]:
            self.sprite.scale_x = 1
            self.xSpeed += self.speed * game.dt
        if abs(self.xSpeed) + abs(self.ySpeed) < .1:
            self.frame = 20 if self.frame >= 24 else self.frame + .3 * game.dt * 30
        else:
            self.frame = 10 if self.frame >= 14 else self.frame + (.05 + math.sqrt(abs(self.xSpeed / 50))) * game.dt
        self.sprite.image = self.seq[round(self.frame)]
        self.xSpeed, self.ySpeed = self.xSpeed / self.drag, \
                                   (self.ySpeed + self.gravity * game.dt) / self.drag
        self.grounded -= game.dt
        print(self.grounded)
        self.collision_check(game)
        self.x, self.y = self.x + self.xSpeed * game.dt, self.y + self.ySpeed * game.dt
        self.window_check(game)
        self.scroll_check(game)


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
            deer.gravity = -abs(deer.gravity)
            deer.sprite.scale_y = -1


class WC:
    pass


class WS(esper.Processor):
    def process(self, dt):
        for ent, (deer, wc) in self.world.get_components(Deer, WC):
            deer.drag = 1


processors = (DPS, AGS, WS)

effects = {
    'none': DPC,
    'AGC': AGC,
    'WC': WC
}
