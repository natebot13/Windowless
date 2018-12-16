import pyglet, math, json, esper
from pyglet.window import key, mouse
from pyglet.gl import *


class Window(pyglet.window.Window):

    def __init__(self, id, effect, fcn):
        self.id = id
        self.effect = effect
        self.moving = False
        self.fcn = functions[fcn] if fcn else functions['follows']
        self.x1 = self.get_location()[0]
        self.x2 = self.get_location()[0] + self.width
        self.y1 = self.get_location()[1]
        self.y2 = self.get_location()[1] + self.height

    def start(self, id, effect, fcn):
        self.id = id
        self.effect = effect
        self.moving = False
        self.fcn = functions[fcn] if fcn else functions['follows']
        self.update((0, 0))
        return self

    def update(self, l):
        self.move(l[0], l[1])
        self.x1 = self.get_location()[0]
        self.x2 = self.get_location()[0] + self.width
        self.y1 = self.get_location()[1]
        self.y2 = self.get_location()[1] + self.height

    def move(self, x, y):
        l = self.fcn(x, y, self)
        if l and l != self.get_location():
            self.set_location(round(l[0]), round(l[1]))

    def on_draw(self):
        self.clear()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        deer.sprite.position = [x_to_window(deer.x, self) + deer.sprite.width * -.5 * deer.sprite.scale_x,
                                y_to_window(deer.y + deer.sprite.height * (deer.sprite.scale_y * .5 - .5), self)]
        BG.blit(x_to_window(0, self), y_to_window(res[1], self))
        deer.sprite.draw()
        for p in platforms:
            pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 0, 2, 3],
                                         ('v2i', points_to_window([p.x1, p.y2, p.x1, p.y1, p.x2, p.y1, p.x2, p.y2], self)),
                                         ('c4B', (p.c * 4)))

    def on_key_press(self, symbol, modifiers):
        if symbol == key.W or symbol == key.SPACE:
            deer.jump()
        if symbol == key.ESCAPE:
            for win in windows:
                win.close()

    def on_mouse_press(self, x, y, buttons, modifiers):
        global mouseLoc
        self.moving = True
        mouseLoc = x, y

    def on_mouse_release(self, x, y, button, modifiers):
        self.moving = False


class Platform:

    def __init__(self, x1, x2, y1, y2, color=(0, 0, 0, 255)):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.c = color


class Trigger(Platform):
    def __init__(self, x1, x2, y1, y2, color=(0, 0, 0, 255)):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.c = color


class Deer:
    def __init__(self, x, y):
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

    def update(self, dt):
        if abs(self.xSpeed) + abs(self.ySpeed) < .1:
            self.frame = 20 if self.frame >= 24 else self.frame + .3 * dt
        else:
            self.frame = 10 if self.frame >= 14 else self.frame + .05 * dt + math.sqrt(abs(self.xSpeed / 50 * dt))
        self.sprite.image = self.seq[round(self.frame)]
        self.xSpeed, self.ySpeed = self.xSpeed / 1.06, (self.ySpeed + self.gravity) / 1.06
        self.grounded = False
        nx, ny = self.x + self.xSpeed * dt, self.y + self.ySpeed * dt
        for p in platforms:
            if p.x1 - self.sprite.width/2 < nx < p.x2 + self.sprite.width/2 and p.y2 + self.sprite.height > ny > p.y1:
                if not p.x1 - self.sprite.width/2 < self.x < p.x2 + self.sprite.width/2:
                    if self.xSpeed > 0:
                        self.xSpeed = p.x1 - self.sprite.width/2 - self.x
                    else:
                        self.xSpeed = p.x2 + self.sprite.width/2 - self.x
                    self.xSpeed /= dt
                if not p.y2 + self.sprite.height > self.y > p.y1:
                    if self.ySpeed < 0:
                        self.ySpeed = p.y2 + self.sprite.height - self.y
                    else:
                        self.grounded = True
                        self.ySpeed = p.y1 - self.y
                    self.ySpeed /= dt
        self.x, self.y = self.x + self.xSpeed * dt, self.y + self.ySpeed * dt
        if world.has_component(deer.id, AGC):
            deer.sprite.scale_y = 1
            world.remove_component(deer.id, AGC)
        if world.has_component(deer.id, WC):
            world.remove_component(deer.id, WC)
        for w in windows:
            if w.x1 - self.sprite.width / 2 < self.x - offset[0] < w.x2 + self.sprite.width / 2 and w.y2 + self.sprite.height > self.y - offset[1] > w.y1 and w.effect:
                world.add_component(self.id, effects[w.effect]() if effects[w.effect] else effects['none'])
        if keys[key.A]:
            self.sprite.scale_x = -1
            self.xSpeed -= .8
        elif keys[key.D]:
            self.sprite.scale_x = 1
            self.xSpeed += .8
        if res[0] + offset[0] < self.x:
            offset[0] += res[0]
        if self.x < offset[0]:
            offset[0] -= res[0]
        if res[1] + offset[1] < self.y:
            offset[1] += res[1]
        if self.y < offset[1]:
            offset[1] -= res[1]


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


def follow(w):
    x, y = int(deer.x - offset[0] - w.width / 2), int(deer.y - offset[1] - w.height / 2)
    if w.width / 2 > deer.x - offset[0]:
        x = 0
    if deer.x - offset[0] > res[0] - (w.width / 2):
        x = res[0] - w.width
    if w.height / 2 > deer.y - offset[1]:
        y = 0
    if deer.y - offset[1] > res[1] - (w.height / 2):
        y = res[1] - w.height
    return x, y


effects = {
    'none': None,
    'AGC': AGC,
    'WC': WC
}
functions = {
    'follows': lambda x, y, w: follow(w),
    'sin': lambda x, y, w: (x, round(math.sin(x/100)*100)+300) if w.moving else False,
    'up left': lambda x, y, w: (x, x-500) if w.moving else False,
    'drag': lambda x, y, w: (x, y) if w.moving else False,
    'half circle': lambda x, y, w: (math.sin((abs(time*4%360-180)-90)/100)*300+800, math.cos((abs(time*4%360-180)-90)/100)*300+400)
}
deer = Deer(10, 0)
BG = pyglet.image.load('bg.png')
keys = key.KeyStateHandler()
res = [0, 0]
time = 0
for m in pyglet.window.get_platform().get_default_display().get_screens():
    if m.width + abs(m.x) > res[0]:
        res[0] = m.width + abs(m.x)
    if m.height + abs(m.y) > res[1]:
        res[1] = m.height + abs(m.y)
offset = [0, 0]
move = [0, 0]
platforms = []
mouseLoc = [0, 0]
windows = [Window(style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS).start(0, None, None)]


def read_map(m='map'):
    with open(m, 'r') as m:
        m = json.loads(m.read())
        platforms.clear()
        for p in m['Platforms']:
            platforms.append(Platform(p['x1'], p['x2'], p['y1'], p['y2'], tuple(p['color'])))
        for w in windows:
            w.close()
        windows.clear()
        for i, w in enumerate(m['Windows']):
            w = Window(style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS, width=w['width'], height=w['height']).start(i+1, w['effect'], w['function'])
            windows.append(w)


def x_to_window(x, w):
    return x - w.x1 - offset[0]


def y_to_window(y, w):
    return w.y2 - y + offset[1]


def points_to_window(p, w):
    return [y_to_window(n, w) if i % 2 else x_to_window(n, w) for i, n in enumerate(p)]


def x_from_window(x, w):
    return x + w.x1 + offset[0]


def y_from_window(y, w):
    return w.y2 - y + offset[1]


def points_from_window(p, w):
    return [y_from_window(n, w) if i % 2 else x_from_window(n, w) for i, n in enumerate(p)]


def update(dt):
    global time
    dt = 1
    time += 1
    for w in windows:
        w.update(points_from_window((w._mouse_x - mouseLoc[0] - offset[0], w._mouse_y - mouseLoc[1] - offset[1]), w))
        w.push_handlers(keys)
    deer.update(dt)
    world.process(dt)


read_map()
world = esper.World()
deer.id = world.create_entity(deer)
world.add_processor(AGS())
world.add_processor(WS())
pyglet.clock.schedule_interval(update, 1/30.0)

pyglet.app.run()
