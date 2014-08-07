from math import sin, cos, radians, pi
import pg

class Window(pg.Window):
    def __init__(self):
        super(Window, self).__init__((800, 600))
        self.wasd = pg.WASD(self, speed=3)
        self.wasd.look_at((-5, 4, 5), (0, 0, 0))
    def setup(self):
        program = pg.Program('shaders/vertex.glsl', 'shaders/fragment.glsl')
        self.context = pg.Context(program)
        self.context.sampler = pg.Texture(0, 'textures/bronze.jpg')
        data = []
        points = pg.poisson_disc(-8, -8, 8, 8, 1, 32)
        for x, z in points:
            noise = pg.simplex2(x * 0.3, z * 0.3, 4)
            y = (noise + 1) / 2
            cylinder = pg.Cylinder((x, 0, z), (x, y, z), 0.4, 18)
            data.extend(pg.interleave(
                cylinder.position, cylinder.normal, cylinder.uv))
        self.context.position, self.context.normal, self.context.uv = (
            pg.VertexBuffer(data).slices(3, 3, 2))
        self.axes = pg.Context(pg.SolidColorProgram())
        self.axes.color = (0.3, 0.3, 0.3)
        self.axes.position = pg.VertexBuffer(pg.Axes(100).position)
    def update(self, t, dt):
        matrix = pg.Matrix().rotate((0, 1, 0), t * 2 * pi / 60)
        self.context.normal_matrix = matrix.inverse().transpose()
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.1, 100)
        self.context.matrix = matrix
        self.axes.matrix = matrix
    def draw(self):
        self.clear()
        self.context.draw(pg.GL_TRIANGLES)
        self.axes.draw(pg.GL_LINES)

if __name__ == "__main__":
    app = pg.App()
    Window()
    app.run()
