from math import sin, cos, radians, pi
import pg

class Window(pg.Window):
    def __init__(self):
        super(Window, self).__init__((800, 600))
        self.wasd = pg.WASD(self)
    def on_size(self, width, height):
        self.aspect = float(width) / height
    def setup(self):
        self.program = pg.Program(
            'shaders/vertex.glsl', 'shaders/fragment.glsl')
        self.context = pg.Context(self.program)
        self.context.sampler = pg.Texture(0, 'textures/earth.png')
        data = []
        for angle in range(0, 360, 30):
            x, z = sin(radians(angle)), cos(radians(angle))
            sphere = pg.Sphere(3, 0.2, (x, 0, z))
            data.extend(pg.interleave(
                [3, 3, 2], [sphere.position, sphere.normal, sphere.uv]))
        vertex_buffer = pg.VertexBuffer(8, data)
        self.context.position = vertex_buffer.slice(3, 0)
        self.context.normal = vertex_buffer.slice(3, 3)
        self.context.uv = vertex_buffer.slice(2, 6)
    def update(self, t, dt):
        matrix = pg.Matrix().rotate((0, 1, 0), t * 2 * pi / 60)
        self.context.normal_matrix = matrix.inverse().transpose()
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
