import pg
import random

COLORS = [
    0x1f77b4, 0xff7f0e, 0x2ca02c, 0xd62728, 0x9467bd,
    0x8c564b, 0xe377c2, 0x7f7f7f, 0xbcbd22, 0x17becf,
]

class Window(pg.Window):
    def __init__(self):
        super(Window, self).__init__((800, 600))
        self.on_size(800, 600)
    def on_size(self, width, height):
        self.aspect = float(width) / height
    def setup(self):
        self.program = pg.Program(
            'shaders/vertex.glsl', 'shaders/fragment.glsl')
        self.context = pg.Context(self.program)
        position = pg.sphere((1.5, 0, 0), 1, 3) + pg.sphere((-1.5, 0, 0), 1, 3)
        color = []
        for _ in xrange(len(position) / 9):
            color.extend(pg.hex_color(random.choice(COLORS)) * 3)
        self.context.position = pg.VertexBuffer(3, position)
        self.context.color = pg.VertexBuffer(3, color)
    def update(self, t, dt):
        matrix = pg.Matrix()
        matrix = matrix.rotate((0, 1, 0), t)
        matrix = matrix.translate((0, 0, -3))
        matrix = matrix.perspective(65, self.aspect, 0.1, 100)
        self.context.matrix = matrix
    def draw(self):
        self.clear()
        self.context.draw(pg.GL_TRIANGLES)
    def teardown(self):
        pass

if __name__ == "__main__":
    app = pg.App()
    Window()
    app.run()
