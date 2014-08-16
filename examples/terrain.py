from collections import defaultdict
import colorsys
import pg

def noise(x, z):
    a = pg.simplex2(-x * 0.01, -z * 0.01, 4)
    b = pg.simplex2(x * 0.1, z * 0.1, 4)
    return (a + 1) * 16 + b / 10

def generate_color(x, z):
    m = 0.005
    h = (pg.simplex2(x * m, z * m, 4) + 1) / 2
    s = (pg.simplex2(-x * m, z * m, 4) + 1) / 2
    v = (pg.simplex2(x * m, -z * m, 4) + 1) / 2
    v = v * 0.5 + 0.5
    return colorsys.hsv_to_rgb(h, s, v)

class Window(pg.Window):
    def setup(self):
        self.wasd = pg.WASD(self, speed=30)
        self.wasd.look_at((-20, 20, -8), (0, 0, 0))
        self.context = pg.Context(pg.DirectionalLightProgram())
        self.context.use_color = True
        self.context.specular_power = 8.0
        self.context.specular_multiplier = 0.3
        normals = defaultdict(list)
        position = []
        normal = []
        color = []
        size = 50
        # generate height map
        height = {}
        colors = {}
        for x in xrange(-size, size + 1):
            for z in xrange(-size, size + 1):
                height[(x, z)] = noise(x, z)
                colors[(x, z)] = generate_color(x, z)
        # generate triangles and track normals for all vertices
        for x in xrange(-size, size):
            for z in xrange(-size, size):
                t1 = [x + 0, z + 0, x + 1, z + 0, x + 0, z + 1]
                t2 = [x + 0, z + 1, x + 1, z + 0, x + 1, z + 1]
                for t in [t1, t2]:
                    x1, z1, x2, z2, x3, z3 = t
                    p1 = (x1, height[(x1, z1)], z1)
                    p2 = (x2, height[(x2, z2)], z2)
                    p3 = (x3, height[(x3, z3)], z3)
                    c1 = colors[(x1, z1)]
                    c2 = colors[(x2, z2)]
                    c3 = colors[(x3, z3)]
                    position.extend([p3, p2, p1])
                    color.extend([c3, c2, c1])
                    n = pg.normalize(pg.cross(pg.sub(p3, p1), pg.sub(p2, p1)))
                    normals[(x1, z1)].append(n)
                    normals[(x2, z2)].append(n)
                    normals[(x3, z3)].append(n)
        # compute average normal for all vertices
        for key, value in normals.items():
            normals[key] = pg.normalize(reduce(pg.add, value))
        for x, y, z in position:
            normal.append(normals[(x, z)])
        # generate vertex buffer
        vb = pg.VertexBuffer(pg.interleave(position, normal, color))
        self.context.position, self.context.normal, self.context.color = (
            vb.slices(3, 3, 3))
    def update(self, t, dt):
        matrix = pg.Matrix()
        matrix = self.wasd.get_matrix(matrix)
        matrix = matrix.perspective(65, self.aspect, 0.1, 1000)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
    def draw(self):
        self.clear()
        self.context.draw(pg.GL_TRIANGLES)

if __name__ == "__main__":
    pg.run(Window)
