from math import sin, cos, radians
import pg
import random

class Window(pg.Window):
    def __init__(self):
        super(Window, self).__init__((800, 600))
        self.wasd = pg.WASD(self, speed=1)
    def on_size(self, width, height):
        self.aspect = float(width) / height
    def setup(self):
        self.program = pg.Program(
            'shaders/vertex.glsl', 'shaders/fragment.glsl')
        self.context = pg.Context(self.program)
        self.context.sampler = pg.Texture(0, 'textures/earth.png')
        position = []
        normal = []
        uv = []
        for angle in range(0, 360, 30):
            x, z = sin(radians(angle)), cos(radians(angle))
            sphere = pg.Sphere(3, 0.2, (x, 0, z))
            position.extend(sphere.position)
            normal.extend(sphere.normal)
            uv.extend(sphere.uv)
        self.context.position = pg.VertexBuffer(3, position)
        self.context.normal = pg.VertexBuffer(3, normal)
        self.context.uv = pg.VertexBuffer(2, uv)
    def update(self, t, dt):
        matrix = pg.Matrix().rotate((0, 1, 0), t)
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
