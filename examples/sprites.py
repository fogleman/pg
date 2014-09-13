from math import sin, cos, pi
import pg

class Window(pg.Window):
    def setup(self):
        self.sheet = pg.SpriteSheet(0, '/Users/fogleman/Desktop/Sprites')
        self.sprites = [
            self.sheet.planet1(),
            self.sheet.planet2(),
            self.sheet.planet3(),
            self.sheet.planet4(),
            self.sheet.planet5(),
            self.sheet.planet6(),
            self.sheet.planet7(),
        ]
        self.context = pg.Context(pg.TextureProgram())
        self.context.sampler = self.sheet
    def update(self, t, dt):
        w, h = self.size
        self.context.matrix = pg.Matrix().orthographic(0, w, 0, h, -1, 1)
        for i, sprite in enumerate(self.sprites):
            x = cos(t + i * 2 * pi / 7) * 200
            y = sin(t + i * 2 * pi / 7) * 200
            sprite.scale = 0.5
            sprite.position = (x + w / 2, y + h / 2)
            sprite.z = i / 10.0
            sprite.rotation = -t
    def draw(self):
        self.clear()
        for sprite in self.sprites:
            sprite.draw(self.context)

if __name__ == "__main__":
    pg.run(Window)
