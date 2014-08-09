import pg
import random

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=32)
        self.wasd.look_at((-10, 0, 0), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.context.use_color = True
        self.context.ambient_color = (0.5, 0.5, 0.5)
        self.context.light_color = (0.5, 0.5, 0.5)
        self.context.light_direction = pg.normalize((-1, 1, 1))
        data = []
        n = 16
        for x in range(256):
            z = random.randint(-n, n)
            y = random.randint(-n, n)
            cuboid = pg.Cuboid(x, x + 1, y - 0.5, y + 0.5, z - 0.5, z + 0.5)
            color = pg.hex_color(random.randint(0, 0xffffff))
            color = [color] * len(cuboid.position)
            data.extend(pg.interleave(
                cuboid.position, cuboid.normal, color))
        self.context.position, self.context.normal, self.context.color = (
            pg.VertexBuffer(data).slices(3, 3, 3))
    def update(self, t, dt):
        matrix = pg.Matrix()
        self.context.model_matrix = matrix
        normal_matrix = matrix.inverse().transpose()
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.1, 1000)
        self.context.matrix = matrix
        self.context.normal_matrix = normal_matrix
        self.context.camera_position = self.wasd.position
    def draw(self):
        self.clear()
        self.context.draw(pg.GL_TRIANGLES)

if __name__ == "__main__":
    app = pg.App()
    Window((800, 600))
    app.run()
