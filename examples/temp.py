from math import sin, cos, radians, pi
import pg

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=3)
        self.wasd.look_at((-5, 4, 5), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        data = []
        points = pg.poisson_disc(-4, -4, 4, 4, 1, 32)
        for x, z in points:
            noise = pg.simplex2(10 + x * 0.25, 10 + z * 0.25, 4)
            y = (noise + 1) / 1
            shape = pg.Cone((x, 0, z), (x, y, z), 0.4, 36)
            data.extend(pg.interleave(shape.position, shape.normal))
            shape = pg.Sphere(3, 0.3, (x, y, z))
            data.extend(pg.interleave(shape.position, shape.normal))
        self.context.position, self.context.normal = (
            pg.VertexBuffer(data).slices(3, 3))
        self.plane = pg.Context(pg.DirectionalLightProgram())
        self.plane.object_color = (1, 1, 1)
        shape = pg.Plane((0, -0.1, 0), (0, 1, 0), 5)
        data = pg.interleave(shape.position, shape.normal)
        self.plane.position, self.plane.normal = (
            pg.VertexBuffer(data).slices(3, 3))
        self.axes = pg.Context(pg.SolidColorProgram())
        self.axes.color = (0.3, 0.3, 0.3)
        self.axes.position = pg.VertexBuffer(pg.Axes(100).position)
    def update(self, t, dt):
        matrix = pg.Matrix()#.rotate((0, 1, 0), t * 2 * pi / 60)
        normal_matrix = matrix.inverse().transpose()
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.01, 100)
        self.context.matrix = matrix
        self.plane.matrix = matrix
        self.axes.matrix = matrix
        self.context.normal_matrix = normal_matrix
        self.plane.normal_matrix = normal_matrix
        self.context.camera_position = self.wasd.position
        self.plane.camera_position = self.wasd.position
    def draw(self):
        self.clear()
        self.plane.draw(pg.GL_TRIANGLES)
        self.context.draw(pg.GL_TRIANGLES)
        self.axes.draw(pg.GL_LINES)

if __name__ == "__main__":
    app = pg.App()
    Window((800, 600))
    app.run()
