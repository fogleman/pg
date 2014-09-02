import pg
import random

SPEED = 250
COUNT = 10000
FIELD_SIZE = 2000
FIELD_DEPTH = 2500

class Window(pg.Window):
    def setup(self):
        data = []
        shape = pg.Plane((0, 0, 0), (0, 0, 1), 0.5, False)
        for _ in xrange(COUNT):
            x = (random.random() - 0.5) * FIELD_SIZE
            y = (random.random() - 0.5) * FIELD_SIZE
            z = random.random() * FIELD_DEPTH
            mesh = pg.Matrix().translate((x, y, z)) * shape
            data.extend(mesh.positions)
        self.context = pg.Context(pg.SolidColorProgram())
        self.context.position = pg.VertexBuffer(data)
    def draw(self):
        self.clear()
        for m in xrange(-1, 2):
            z = m * FIELD_DEPTH + (-self.t * SPEED) % FIELD_DEPTH
            matrix = pg.Matrix().translate((0, 0, -z))
            matrix = matrix.perspective(65, self.aspect, 1, 1000)
            self.context.matrix = matrix
            self.context.camera_position = (0, 0, z)
            self.context.draw()

if __name__ == "__main__":
    pg.run(Window)
