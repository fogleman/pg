from math import sin, cos, pi
import pg

RED = 0xF04326
YELLOW = 0xFAC02D
GREEN = 0x1AB243
BLUE = 0x1256D1

COLORS = [pg.hex_color(x) for x in [RED, YELLOW, GREEN, BLUE]]

class Window(pg.Window):
    def setup(self):
        self.font = pg.Font(self, 0, '/Library/Fonts/Arial.ttf', 24)
        self.wasd = pg.WASD(self, speed=5)
        self.wasd.look_at((14, 0, 0), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.sphere = pg.Sphere(5, 0.4, (0, 0, 0))
        self.context.ambient_color = (0.4, 0.4, 0.4)
        self.context.light_color = (0.6, 0.6, 0.6)
    def draw(self):
        self.clear()
        self.context.camera_position = self.wasd.position
        matrix = self.wasd.get_matrix()
        matrix = matrix.perspective(65, self.aspect, 0.01, 100)
        for z in range(-2, 3):
            for x in range(-10, 11):
                y = sin(self.time * pi / 4 + x * 0.5 + z * pi) * 3
                model_matrix = pg.Matrix().translate((x, y, z * 3))
                self.context.model_matrix = model_matrix
                self.context.matrix = matrix * model_matrix
                self.context.object_color = COLORS[(z + x) % len(COLORS)]
                self.sphere.draw(self.context)
        w, h = self.size
        self.font.render('%.1f fps' % self.fps, (w - 5, 0), (1, 0))
        text = 'x=%.2f, y=%.2f, z=%.2f' % self.wasd.position
        self.font.render(text, (5, 0))

if __name__ == "__main__":
    pg.run(Window)
