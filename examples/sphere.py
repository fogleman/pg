import pg

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self)
        self.wasd.look_at((-1, 1, 1), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        sphere = pg.Sphere(4, 0.5, (0, 0, 0))
        self.context.position = pg.VertexBuffer(sphere.position)
        self.context.normal = pg.VertexBuffer(sphere.normal)
    def update(self, t, dt):
        matrix = pg.Matrix()
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.01, 100)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
    def draw(self):
        self.clear()
        self.context.draw(pg.GL_TRIANGLES)

if __name__ == "__main__":
    app = pg.App()
    Window((800, 600))
    app.run()
