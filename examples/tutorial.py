import pg

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self)
        self.wasd.look_at((0, 0, 2), (0, 0, 0))
        self.program = pg.DirectionalLightProgram()
        self.context = pg.Context(self.program)
        sphere = pg.Sphere(3, 0.5, (0, 0, 0))
        self.context.position = pg.VertexBuffer(sphere.positions)
        self.context.normal = pg.VertexBuffer(sphere.normals)
    def update(self, t, dt):
        matrix = self.wasd.get_matrix()
        matrix = matrix.perspective(65, self.aspect, 0.1, 100)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
    def draw(self):
        self.clear()
        self.context.draw()

if __name__ == "__main__":
    pg.run(Window)
