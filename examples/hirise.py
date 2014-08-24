from collections import defaultdict
import pg

STEP = 32
HEIGHT = 10
SPEED = 1200

class Window(pg.Window):
    def setup(self):
        self.set_clear_color(0.87, 0.81, 0.70)
        self.wasd = pg.WASD(self, speed=SPEED)
        self.wasd.look_at((0, 0, 0), (30, -5, 30))
        self.context = pg.Context(Program())
        self.context.specular_multiplier = 0.25
        self.context.object_color = (0.48, 0.36, 0.22)
        self.context.ambient_color = (0.5, 0.5, 0.5)
        self.context.light_color = (0.5, 0.5, 0.5)
        self.context.light_direction = pg.normalize((-1, 1, 1))
        self.context.normal_sampler = pg.Texture(0, 'examples/output.png')
        try:
            self.context.sampler = pg.Texture(1, 'examples/texture.jp2')
            self.context.use_texture = True
        except IOError:
            self.context.use_texture = False
        mesh = pg.STL('examples/output.stl').center()
        (x0, y0, z0), (x1, y1, z1) = pg.bounding_box(mesh.positions)
        print (x0, y0, z0), (x1, y1, z1)
        for x, y, z in mesh.positions:
            u = (z - z0) / (z1 - z0)
            v = 1 - (x - x0) / (x1 - x0)
            mesh.uvs.append((u, v))
        self.context.position = pg.VertexBuffer(mesh.positions)
        self.context.uv = pg.VertexBuffer(mesh.uvs)
        p = mesh.positions
        self.lookup = defaultdict(list)
        for v1, v2, v3 in zip(p[::3], p[1::3], p[2::3]):
            x, y, z = v1
            x, z = int(round(x / STEP)), int(round(z / STEP))
            self.lookup[(x, z)].append((v1, v2, v3))
    def adjust_height(self):
        o = x, y, z = self.wasd.position
        d = (0, -1, 0)
        x, z = int(round(x / STEP)), int(round(z / STEP))
        for i in xrange(x - 1, x + 2):
            for j in xrange(z - 1, z + 2):
                for v1, v2, v3 in self.lookup[(i, j)]:
                    t = pg.ray_triangle_intersection(v1, v2, v3, o, (0, -1, 0))
                    if t and t < HEIGHT:
                        self.wasd.y -= t - HEIGHT
                        return
                    t = pg.ray_triangle_intersection(v1, v2, v3, o, (0, 1, 0))
                    if t:
                        self.wasd.y += t + HEIGHT
                        return
    def draw(self):
        self.adjust_height()
        self.clear()
        matrix = self.wasd.get_matrix()
        matrix = matrix.perspective(65, self.aspect, 1, 100000)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
        self.context.draw()

class Program(pg.Program):
    VS = '''
    #version 120

    uniform mat4 matrix;
    uniform mat4 model_matrix;

    attribute vec4 position;
    attribute vec2 uv;

    varying vec3 frag_position;
    varying vec2 frag_uv;

    void main() {
        gl_Position = matrix * position;
        frag_position = vec3(model_matrix * position);
        frag_uv = uv;
    }
    '''
    FS = '''
    #version 120

    uniform sampler2D sampler;
    uniform sampler2D normal_sampler;
    uniform vec3 camera_position;

    uniform mat4 normal_matrix;
    uniform vec3 light_direction;
    uniform vec3 object_color;
    uniform vec3 ambient_color;
    uniform vec3 light_color;
    uniform float specular_power;
    uniform float specular_multiplier;
    uniform bool use_texture;

    varying vec3 frag_position;
    varying vec2 frag_uv;

    void main() {
        vec3 norm = vec3(texture2D(normal_sampler, frag_uv));
        norm = norm * vec3(2.0) - vec3(1.0);
        norm = norm.xzy;
        vec3 color = object_color;
        if (use_texture) {
            color = color * 0.6 + color * vec3(texture2D(sampler, frag_uv)) * 0.4;
        }
        float diffuse = max(dot(mat3(normal_matrix) * norm,
            light_direction), 0.0);
        float specular = 0.0;
        if (diffuse > 0.0) {
            vec3 camera_vector = normalize(camera_position - frag_position);
            specular = pow(max(dot(camera_vector,
                reflect(-light_direction, norm)), 0.0), specular_power);
        }
        vec3 light = ambient_color + light_color * diffuse +
            specular * specular_multiplier;
        gl_FragColor = vec4(min(color * light, vec3(1.0)), 1.0);
    }
    '''
    def __init__(self):
        super(Program, self).__init__(self.VS, self.FS)
    def set_defaults(self, context):
        context.model_matrix = pg.Matrix()
        context.normal_matrix = pg.Matrix().inverse().transpose()
        context.light_direction = pg.normalize((1, 1, 1))
        context.object_color = (0.4, 0.6, 0.8)
        context.ambient_color = (0.3, 0.3, 0.3)
        context.light_color = (0.7, 0.7, 0.7)
        context.specular_power = 32.0
        context.specular_multiplier = 1.0
        context.use_texture = False
        context.use_color = False

if __name__ == "__main__":
    pg.run(Window)
