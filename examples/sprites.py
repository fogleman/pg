from math import sin, cos, pi
import pg

class Window(pg.Window):
    def setup(self):
        sheet = pg.SpriteSheet(0, '/Users/fogleman/Desktop/Sprites')
        self.batch = pg.SpriteBatch(sheet)
        sheet.planet1(self.batch)
        sheet.planet2(self.batch)
        sheet.planet3(self.batch)
        sheet.planet4(self.batch)
        sheet.planet5(self.batch)
        sheet.planet6(self.batch)
        sheet.planet7(self.batch)
    def update(self, t, dt):
        w, h = self.size
        for i, sprite in enumerate(self.batch.sprites):
            x = cos(t + i * 2 * pi / 7) * 200
            y = sin(t + i * 2 * pi / 7) * 200
            sprite.scale = 0.5
            sprite.position = (x + w / 2, y + h / 2)
            sprite.z = i / 10.0
            sprite.rotation = -t
    def draw(self):
        self.clear()
        self.batch.draw()

if __name__ == "__main__":
    pg.run(Window)
