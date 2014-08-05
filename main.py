from math import sin, cos, radians
import pg
import random

class Window(pg.Window):
    def __init__(self):
        super(Window, self).__init__((800, 600))
        self.set_exclusive()
        self.wasd = pg.WASD(self, speed=3)
    def on_size(self, width, height):
        self.aspect = float(width) / height
    def setup(self):
        self.program = pg.Program(
            'shaders/vertex.glsl', 'shaders/fragment.glsl')
        self.context = pg.Context(self.program)
        position = []
        for angle in xrange(0, 360, 30):
            x, z = sin(radians(angle)), cos(radians(angle))
            position.extend(pg.sphere(3, 0.2, (x, 0, z)))
        color = []
        for i in xrange(12 * 8):
            n = len(position) / 3 / 12 / 8
            color.extend(pg.hex_color(random.randint(0, 0xffffff)) * n)
        self.context.position = pg.VertexBuffer(3, position)
        self.context.color = pg.VertexBuffer(3, color)
    def update(self, t, dt):
        matrix = pg.Matrix().rotate((0, 1, 0), t)
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.1, 100)
        self.context.matrix = matrix
    def draw(self):
        self.clear()
        self.context.draw(pg.GL_TRIANGLES)

if __name__ == "__main__":
    app = pg.App()
    Window()
    app.run()
