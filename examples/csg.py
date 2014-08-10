import pg

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=5)
        self.wasd.look_at((-3, 3, 3), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        a = pg.CSG(pg.Cuboid(-1, 1, -1, 1, -1, 1))
        b = pg.CSG(pg.Sphere(2, 1.35))
        c = pg.CSG(pg.Cylinder((-1, 0, 0), (1, 0, 0), 0.5, 18))
        d = pg.CSG(pg.Cylinder((0, -1, 0), (0, 1, 0), 0.5, 18))
        e = pg.CSG(pg.Cylinder((0, 0, -1), (0, 0, 1), 0.5, 18))
        shape = (a & b) - (c | d | e)
        position, normal = shape.triangulate()
        self.context.position = pg.VertexBuffer(position)
        self.context.normal = pg.VertexBuffer(normal)
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
    Window()
    app.run()
