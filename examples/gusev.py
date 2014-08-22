from collections import defaultdict
import pg

# download the gusev.stl file here:
# http://www.michaelfogleman.com/static/gusev.stl.zip

class Window(pg.Window):
    def setup(self):
        self.set_clear_color(0.87, 0.81, 0.70)
        self.wasd = pg.WASD(self, speed=10)
        self.wasd.look_at((0, 0, 0), (30, -5, 30))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.context.specular_multiplier = 0.25
        self.context.ambient_color = (0.5, 0.5, 0.5)
        self.context.light_color = (0.5, 0.5, 0.5)
        self.context.use_texture = True
        self.context.sampler = pg.Texture(0, 'examples/gusev.jpg')
        mesh = pg.STL('examples/gusev.stl').smooth_normals()
        (x0, y0, z0), (x1, y1, z1) = pg.bounding_box(mesh.positions)
        for x, y, z in mesh.positions:
            u = 1 - (z - z0) / (z1 - z0)
            v = 1 - (x - x0) / (x1 - x0)
            mesh.uvs.append((u, v))
        self.mesh = mesh
        p = self.mesh.positions
        self.lookup = defaultdict(list)
        for v1, v2, v3 in zip(p[::3], p[1::3], p[2::3]):
            x, y, z = v1
            x, z = int(round(x)), int(round(z))
            self.lookup[(x, z)].append((v1, v2, v3))
    def adjust_height(self):
        o = x, y, z = self.wasd.position
        d = (0, -1, 0)
        x, z = int(round(x)), int(round(z))
        for i in xrange(x - 1, x + 2):
            for j in xrange(z - 1, z + 2):
                for v1, v2, v3 in self.lookup[(i, j)]:
                    t = pg.ray_triangle_intersection(v1, v2, v3, o, d)
                    if t and t < 1:
                        self.wasd.y += 1 - t
                        return
    def draw(self):
        self.adjust_height()
        self.clear()
        matrix = self.wasd.get_matrix()
        matrix = matrix.perspective(65, self.aspect, 0.1, 1000)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
        self.mesh.draw(self.context)

if __name__ == "__main__":
    pg.run(Window)
