from math import sin, cos
import pg

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=5)
        self.wasd.look_at((-12, 0, 4), (-6, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        sphere = pg.Sphere(3, 0.4, (0, 0, 0))
        self.context.position = pg.VertexBuffer(sphere.position)
        self.context.normal = pg.VertexBuffer(sphere.normal)
        self.context.normal_matrix = pg.Matrix().inverse().transpose()
    def draw(self):
        self.clear()
        self.context.camera_position = self.wasd.position
        for x in range(-10, 11):
            y = sin(self.time * 2 + x * 0.5) * 2
            matrix = pg.Matrix().translate((x, y, 0))
            matrix = self.wasd.get_matrix(matrix)
            matrix = matrix.perspective(65, self.aspect, 0.01, 100)
            self.context.matrix = matrix
            self.context.draw(pg.GL_TRIANGLES)

if __name__ == "__main__":
    app = pg.App()
    Window((800, 600))
    app.run()
