from OpenGL.GL import glClearColor
import pg

# download the .stl file here:
# http://www.thingiverse.com/thing:429480

class Window(pg.Window):
    def setup(self):
        glClearColor(0.87, 0.81, 0.70, 1.00)
        self.wasd = pg.WASD(self, speed=20)
        self.wasd.look_at((-55, 20, -5), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.context.specular_multiplier = 0.25
        self.context.ambient_color = (0.5, 0.5, 0.5)
        self.context.light_color = (0.5, 0.5, 0.5)
        self.context.use_texture = True
        self.context.sampler = pg.Texture(0, 'examples/gusev.jpg')
        # self.context.normal_sampler = pg.Texture(1, 'examples/normal_sand.jpg')
        mesh = pg.STL('examples/gusev.stl')
        mesh = mesh.reverse_winding().swap_axes(1, 2, 0).smooth_normals()
        minx, minz = -90.0, -57.6337509155
        maxx, maxz = 47.7562522888, 93.75
        for x, y, z in mesh.positions:
            u = 1 - (z - minz) / (maxz - minz)
            v = 1 - (x - minx) / (maxx - minx)
            mesh.uvs.append((u, v))
        self.mesh = mesh
    def update(self, t, dt):
        matrix = pg.Matrix()
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.1, 1000)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
    def draw(self):
        self.clear()
        self.mesh.draw(self.context)

if __name__ == "__main__":
    pg.run(Window)
