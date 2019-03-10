import pyglet, math
from gameobject import GameObject
from pyglet.window import key


class Deer(GameObject):
    def __init__(self, game, x: float, y: float):
        super().__init__(game, x, y)
        self.jumpStrength = 1500.0
        self.seq = pyglet.image.ImageGrid(pyglet.resource.image('deer.png'), 5, 5)
        self.sprite = pyglet.sprite.Sprite(img=self.seq[self.frame])

    def jump(self, dt):
        if self.grounded > 0:
            self.ySpeed -= self.jumpStrength
            self.grounded = 0

    def scroll_check(self):
        if self.game.res[0] + self.game.offset[0] < self.x + self.sprite.width:
            self.game.offset[0] += self.game.res[0]
        if self.x < self.game.offset[0]:
            self.game.offset[0] -= self.game.res[0]
        if self.game.res[1] + self.game.offset[1] < self.y:
            self.game.offset[1] += self.game.res[1]
        if self.y < self.game.offset[1]:
            self.game.offset[1] -= self.game.res[1]

    def update(self):
        super().update()
        if self.game.keys[key.A]:
            self.sprite.scale_x = -1
            self.xSpeed -= self.speed * self.game.dt
        elif self.game.keys[key.D]:
            self.sprite.scale_x = 1
            self.xSpeed += self.speed * self.game.dt
        if abs(self.xSpeed) + abs(self.ySpeed) < .1:
            self.frame = 20 if self.frame >= 24 else self.frame + .3 * self.game.dt * 30
        else:
            self.frame = 10 if self.frame >= 14 else self.frame + (.05 + math.sqrt(abs(self.xSpeed / 50))) * self.game.dt
        self.sprite.image = self.seq[round(self.frame)]
        self.scroll_check()

