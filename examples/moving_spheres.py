from math import sin, cos, pi
import pg

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=5)
        self.wasd.look_at((14, 0, 0), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        sphere = pg.Sphere(3, 0.4, (0, 0, 0))
        self.context.position = pg.VertexBuffer(sphere.position)
        self.context.normal = pg.VertexBuffer(sphere.normal)
    def draw(self):
        self.clear()
        self.context.camera_position = self.wasd.position
        matrix = self.wasd.get_matrix()
        matrix = matrix.perspective(65, self.aspect, 0.01, 100)
        for z in range(-2, 3):
            for x in range(-10, 11):
                y = sin(self.time * pi + x * 0.5 + z * pi) * 3
                model_matrix = pg.Matrix().translate((x, y, z * 3))
                self.context.model_matrix = model_matrix
                self.context.matrix = matrix * model_matrix
                self.context.draw(pg.GL_TRIANGLES)

if __name__ == "__main__":
    app = pg.App()
    Window()
    app.run()
