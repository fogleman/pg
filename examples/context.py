import pg

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self)
        self.wasd.look_at((0, 0, 4), (0, 0, 0))
        self.program = pg.DirectionalLightProgram()
        self.context1 = pg.Context(self.program)
        self.context2 = pg.Context(self.program)
        sphere = pg.Sphere(4, 0.5, (2, 0, 0))
        self.context1.position = pg.VertexBuffer(sphere.position)
        self.context1.normal = pg.VertexBuffer(sphere.normal)
        sphere = pg.Sphere(4, 0.5, (-2, 0, 0))
        self.context2.position = pg.VertexBuffer(sphere.position)
        self.context2.normal = pg.VertexBuffer(sphere.normal)
    def update(self, t, dt):
        matrix = pg.Matrix()
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.01, 100)
        self.context1.matrix = matrix
        self.context1.camera_position = self.wasd.position
        self.context1.object_color = (1.0, 0.2, 0.0)
        self.context2.matrix = matrix
        self.context2.camera_position = self.wasd.position
    def draw(self):
        self.clear()
        self.context1.draw(pg.GL_TRIANGLES)
        self.context2.draw(pg.GL_TRIANGLES)

if __name__ == "__main__":
    pg.run(Window)
