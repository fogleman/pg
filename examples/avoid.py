from math import sin, cos, pi, atan2, hypot
import pg
import random

SPEED = 50

class Bot(object):
    def __init__(self, position, target):
        self.y = (random.random() - 0.5) * 20
        self.position = position
        self.target = target
        self.speed = random.random() + 0.5
        self.padding = random.random() * 8 + 16
        self.angle = 0
    def get_position(self, offset):
        px, py = self.position
        # tx, ty = self.target
        angle = self.angle# or atan2(ty - py, tx - px)
        return (px + cos(angle) * offset, py + sin(angle) * offset)
    def update(self, bots):
        px, py = self.position
        tx, ty = self.target
        angle = atan2(ty - py, tx - px)
        dx = cos(angle)
        dy = sin(angle)
        for bot in bots:
            if bot == self:
                continue
            x, y = bot.position
            d = hypot(px - x, py - y) ** 2
            p = bot.padding ** 2
            angle = atan2(py - y, px - x)
            dx += cos(angle) / d * p
            dy += sin(angle) / d * p
        angle = atan2(dy, dx)
        magnitude = hypot(dx, dy)
        self.angle = angle
        return angle, magnitude
    def set_position(self, position):
        self.position = position

class Model(object):
    def __init__(self, width, height, count):
        self.width = width
        self.height = height
        self.bots = self.create_bots(count)
    def create_bots(self, count):
        result = []
        for i in range(count):
            position = self.select_point()
            target = self.select_point()
            bot = Bot(position, target)
            result.append(bot)
        return result
    def select_point(self):
        cx = self.width / 2.0
        cy = self.height / 2.0
        radius = min(self.width, self.height) * 0.4
        angle = random.random() * 2 * pi
        x = cx + cos(angle) * radius
        y = cy + sin(angle) * radius
        return (x, y)
    def update(self, dt):
        data = [bot.update(self.bots) for bot in self.bots]
        for bot, (angle, magnitude) in zip(self.bots, data):
            speed = min(1, 0.2 + magnitude * 0.8)
            dx = cos(angle) * dt * SPEED * bot.speed * speed
            dy = sin(angle) * dt * SPEED * bot.speed * speed
            px, py = bot.position
            tx, ty = bot.target
            bot.set_position((px + dx, py + dy))
            if hypot(px - tx, py - ty) < 10:
                bot.target = self.select_point()

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=100)
        self.wasd.look_at((300, 15, 300), (0, -50, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.target = pg.Sphere(3, 2)
        a = pg.Solid(pg.Sphere(3, 4))
        b = pg.Solid(pg.Sphere(2, 2, (3, 0, 0)))
        c = pg.Solid(pg.Cylinder((-6, 0, 0), (0, 0, 0), 2, 16))
        d = pg.Solid(pg.Sphere(2, 2, (-6, 0, 0)))
        solid = (a - b) | c | d
        self.mesh = solid.mesh()
        self.model = Model(400, 400, 100)
    def set_matrix(self, x, y, z, a):
        matrix = pg.Matrix().rotate((0, 1, 0), a).translate((x, y, z))
        inverse = pg.Matrix().rotate((0, 1, 0), -a)
        self.context.light_direction = inverse * pg.normalize((1, 1, 1))
        self.context.camera_position = matrix.inverse() * self.wasd.position
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.1, 1000)
        self.context.matrix = matrix
        # mesh.draw(self.context)
    def update(self, t, dt):
        self.clear()
        self.model.update(dt)
        bot = self.model.bots[0]
        # setup camera
        x1, z1 = bot.get_position(0)
        x2, z2 = bot.get_position(50)
        # self.wasd.look_at((x1, bot.y, z1), (x2, bot.y, z2))
        # self.wasd.look_at(self.wasd.position, (x1, bot.y, z1))
        # draw target
        self.context.object_color = (1, 0, 0)
        x, z = bot.target
        self.set_matrix(x, bot.y, z, 0)
        self.target.draw(self.context)
        # draw bots
        self.context.object_color = (0.4, 0.6, 0.8)
        for bot in self.model.bots:
            x, z = bot.position
            self.set_matrix(x, bot.y, z, bot.angle)
            self.mesh.draw(self.context)

if __name__ == "__main__":
    pg.run(Window)
