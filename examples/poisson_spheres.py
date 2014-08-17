import pg

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=10)
        self.wasd.look_at((0, 3, 12), (0, 0, 7))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.points = pg.poisson_disc(-10, -10, 10, 10, 1.5, 32)
        self.mats = [pg.Matrix().translate((x, 0, z)) for x, z in self.points]
        self.sphere = pg.Sphere(4, 0.7)
    def draw(self):
        self.clear()
        self.context.camera_position = self.wasd.position
        matrix = self.wasd.get_matrix()
        matrix = matrix.perspective(65, self.aspect, 0.01, 100)
        for (x, z), mat in zip(self.points, self.mats):
            self.context.model_matrix = mat
            self.context.matrix = matrix * mat
            self.sphere.draw(self.context)

if __name__ == "__main__":
    pg.run(Window)
