import pg

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self)
        self.wasd.look_at((0, 0, 3), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.mesh = pg.OBJ('examples/suzanne.obj').centered().smoothed()
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
