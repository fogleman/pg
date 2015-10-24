import pg

class Window(pg.Window):
    def setup(self):
        self.font = pg.Font(self, 1, '/Library/Fonts/Arial.ttf', 24)
        self.wasd = pg.WASD(self)
        self.wasd.look_at(pg.normalize((1, 0, 1)), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.context.sampler = pg.Texture(0, 'examples/earth.png')
        self.context.use_texture = True
        sphere = pg.Sphere(4, 0.5, (0, 0, 0))
        self.context.position = pg.VertexBuffer(sphere.positions)
        self.context.normal = pg.VertexBuffer(sphere.normals)
        self.context.uv = pg.VertexBuffer(sphere.uvs)
    def update(self, t, dt):
        matrix = pg.Matrix()
        self.context.model_matrix = matrix
        normal_matrix = matrix.inverse().transpose()
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.01, 100)
        self.context.matrix = matrix
        self.context.normal_matrix = normal_matrix
        self.context.camera_position = self.wasd.position
    def draw(self):
        self.clear()
        self.context.draw()
        w, h = self.size
        self.font.render('%.1f fps' % self.fps, (w - 5, 0), (1, 0))
        text = 'x=%.2f, y=%.2f, z=%.2f' % self.wasd.position
        self.font.render(text, (5, 0))

if __name__ == "__main__":
    pg.run(Window)
