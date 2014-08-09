import pg
import random

class Bullet(object):
    def __init__(self, t, position, vector):
        self.time = t
        self.position = position
        self.vector = vector

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=8)
        self.wasd.look_at((-10, 0, 0), (0, 0, 0))
        # cuboids
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
        # bullets
        self.bullet = pg.Context(pg.DirectionalLightProgram())
        self.bullet.ambient_color = (0.5, 0.5, 0.5)
        self.bullet.light_color = (0.5, 0.5, 0.5)
        sphere = pg.Sphere(3, 0.05, (0, 0, 0))
        self.bullet.position = pg.VertexBuffer(sphere.position)
        self.bullet.normal = pg.VertexBuffer(sphere.normal)
        self.bullets = []
    def draw(self):
        self.clear()
        self.context.camera_position = self.wasd.position
        self.bullet.camera_position = self.wasd.position
        matrix = self.wasd.get_matrix()
        matrix = matrix.perspective(65, self.aspect, 0.1, 500)
        self.context.matrix = matrix
        self.context.draw(pg.GL_TRIANGLES)
        for bullet in list(self.bullets):
            dt = self.time - bullet.time
            x, y, z = pg.add(bullet.position, pg.mul(bullet.vector, dt * 16))
            model_matrix = pg.Matrix().translate((x, y, z))
            self.bullet.model_matrix = model_matrix
            self.bullet.matrix = matrix * model_matrix
            self.bullet.draw(pg.GL_TRIANGLES)
            if dt > 10:
                self.bullets.remove(bullet)
    def on_mouse_button(self, button, action, mods):
        if button == 0 and action == 1:
            bullet = Bullet(
                self.time, self.wasd.position, self.wasd.get_sight_vector())
            self.bullets.append(bullet)

if __name__ == "__main__":
    app = pg.App()
    Window()
    app.run()
