from util import x_to_pixels, y_to_pixels

class GameObject:
    def __init__(self, game, x: float, y: float):
        self.game = game
        self.x = x_to_pixels(game, x)
        self.y = y_to_pixels(game, y)
        self.dead = False
        self.grounded = 0
        self.xSpeed = 0.0
        self.ySpeed = 0.0
        self.frame = 10
        self.drag = 1.06
        self.gravity = 1500.0
        self.speed = 1500.0

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

    def update(self):
        self.xSpeed, self.ySpeed = self.xSpeed / self.drag, \
                                   (self.ySpeed + self.gravity * self.game.dt) / self.drag
        self.collision_check(self.game)
        self.x, self.y = self.x + self.xSpeed * self.game.dt, self.y + self.ySpeed * self.game.dt
        self.grounded -= self.game.dt

    def kill(self):
        self.dead = True


