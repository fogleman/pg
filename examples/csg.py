import pg

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=5)
        self.wasd.look_at((-2, 2, 2), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.context.sampler = pg.Texture(0, 'examples/bronze.jpg')
        self.context.use_texture = True
        a = pg.Solid(pg.Cuboid(-1, 1, -1, 1, -1, 1))
        b = pg.Solid(pg.Sphere(2, 1.35))
        c = pg.Solid(pg.Cylinder((-1, 0, 0), (1, 0, 0), 0.5, 18))
        d = pg.Solid(pg.Cylinder((0, -1, 0), (0, 1, 0), 0.5, 18))
        e = pg.Solid(pg.Cylinder((0, 0, -1), (0, 0, 1), 0.5, 18))
        solid = (a & b) - (c | d | e)
        self.mesh = solid.mesh()
    def update(self, t, dt):
        matrix = pg.Matrix()
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.01, 100)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
    def draw(self):
        self.clear()
        self.mesh.draw(self.context)

if __name__ == "__main__":
    pg.run(Window)
