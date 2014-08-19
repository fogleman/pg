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
            data.extend(pg.interleave(mesh.positions, mesh.normals))
        self.vb = pg.VertexBuffer(data)
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.context.light_direction = (0, 0, 1)
        self.context.object_color = (1, 1, 1)
        self.context.position, self.context.normal = self.vb.slices(3, 3)
    def draw(self):
        self.clear()
        for m in xrange(-1, 2):
            z = m * FIELD_DEPTH + (-self.time * SPEED) % FIELD_DEPTH
            matrix = pg.Matrix().translate((0, 0, -z))
            matrix = matrix.perspective(65, self.aspect, 1, 1000)
            self.context.matrix = matrix
            self.context.camera_position = (0, 0, z)
            self.context.draw()

if __name__ == "__main__":
    pg.run(Window)
