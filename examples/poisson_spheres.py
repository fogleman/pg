import pg

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=3)
        self.wasd.look_at((0, 12, 6), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        sphere = pg.Sphere(3, 0.4, (0, 0, 0))
        data = []
        points = pg.poisson_disc(-10, -10, 10, 10, 1, 32)
        for x, z in points:
            matrix = pg.Matrix().translate((x, 0, z))
            position = [matrix * p for p in sphere.position]
            data.extend(pg.interleave(position, sphere.normal))
        self.context.position, self.context.normal = (
            pg.VertexBuffer(data).slices(3, 3))
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
