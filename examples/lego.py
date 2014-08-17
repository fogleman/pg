from math import sin, cos, pi
import pg
import random

class LegoMan(object):
    def __init__(self):
        self.x = (random.random() - 0.5) * 50
        self.z = (random.random() - 0.5) * 50
        self.a = random.random() * pi * 2
    def update(self, t, dt):
        if random.random() < 0.02:
            self.a += random.randint(-1, 1) * pi / 8
        dx = cos(self.a)
        dz = sin(self.a)
        self.x += dx * dt
        self.z += dz * dt

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=10)
        self.wasd.look_at((0, 8, 30), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.mesh = pg.OBJ('examples/lego.obj').centered().smoothed()
        self.men = [LegoMan() for _ in xrange(50)]
    def update(self, t, dt):
        self.wasd.y = 1.5
        self.clear()
        for man in self.men:
            man.update(t, dt)
            a = man.a + pi / 2
            matrix = pg.Matrix().rotate((0, 1, 0), a).translate((-man.x, 0, -man.z))
            inverse = pg.Matrix().rotate((0, 1, 0), -a)
            self.context.light_direction = inverse * pg.normalize((1, 1, 1))
            self.context.camera_position = matrix.inverse() * self.wasd.position
            matrix = self.wasd.get_matrix(matrix)
            matrix = matrix.perspective(65, self.aspect, 0.1, 1000)
            self.context.matrix = matrix
            self.mesh.draw(self.context)

if __name__ == "__main__":
    pg.run(Window)
