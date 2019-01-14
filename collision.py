class Platform:

    def __init__(self, x1: float, x2: float, y1: float, y2: float):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def collide_x(self, x: float, width: float):
        return self.x1 - width < x < self.x2

    def collide_y(self, y: float, height: float):
        return self.y1 < y < self.y2 + height

    def collide(self, x: float, y: float, width: float, height: float):
        return self.collide_x(x, width) and self.collide_y(y, height)
