from collections import defaultdict
from math import atan2
import pg

NAME = 'PSP_009149_1750'
STEP = 16
HEIGHT = 1.8288 * 10
SPEED = 1.34 * 500

class LoadingScene(pg.Scene):
    def setup(self):
        self.message = ''
        self.triangles = 0
        fg = (0, 0, 0, 1)
        self.title_font = pg.Font(self, 2, '/Library/Fonts/Arial.ttf', 72, fg)
        self.font = pg.Font(self, 3, '/Library/Fonts/Arial.ttf', 36, fg)
    def enter(self):
        context = pg.Context(Program())
        self.set_message('loading color texture')
        context.sampler = pg.Texture(1, 'examples/%s.jpg' % NAME)
        self.set_message('loading normal texture')
        context.normal_sampler = pg.Texture(0, 'examples/%s.png' % NAME)
        self.set_message('loading mesh')
        mesh = pg.STL('examples/%s.stl' % NAME).center()
        (x0, y0, z0), (x1, y1, z1) = pg.bounding_box(mesh.positions)
        context.uv0 = (x0, z0)
        context.uv1 = (x1, z1)
        self.set_message('generating vertex buffer')
        context.position = pg.VertexBuffer(mesh.positions)
        self.set_message('generating height map')
        p = mesh.positions
        lookup = defaultdict(list)
        for v1, v2, v3 in zip(p[::3], p[1::3], p[2::3]):
            x, y, z = v1
            x, z = int(round(x / STEP)), int(round(z / STEP))
            lookup[(x, z)].append((v1, v2, v3))
        self.set_message('%d triangles' % (len(p) / 3))
        self.window.set_scene(MainScene(self.window, context, lookup))
    def set_message(self, message):
        self.message = message
        self.window.redraw()
        pg.poll_events()
    def draw(self):
        self.window.clear()
        w, h = self.window.size
        title = 'Mars HiRISE Viewer'
        self.title_font.render(title, (w / 2, h / 2 - 10), (0.5, 1))
        self.font.render(self.message, (w / 2, h / 2 + 10), (0.5, 0))
        self.font.render(NAME, (w / 2, h - 50), (0.5, 1))

class MainScene(pg.Scene):
    def __init__(self, window, context, lookup):
        super(MainScene, self).__init__(window)
        self.context = context
        self.lookup = lookup
    def setup(self):
        fg = (0, 0, 0, 1)
        self.font = pg.Font(self, 2, '/Library/Fonts/Arial.ttf', 24, fg)
        self.window.set_clear_color(0.74, 0.70, 0.64)
        self.wasd = pg.WASD(self, speed=SPEED)
        self.dy = 0
    def get_height(self):
        p = x, y, z = self.wasd.position
        x, z = int(round(x / STEP)), int(round(z / STEP))
        for i in xrange(x - 1, x + 2):
            for j in xrange(z - 1, z + 2):
                for v1, v2, v3 in self.lookup[(i, j)]:
                    t = pg.ray_triangle_intersection(v1, v2, v3, p, (0, -1, 0))
                    if t:
                        return t
                    t = pg.ray_triangle_intersection(v1, v2, v3, p, (0, 1, 0))
                    if t:
                        return -t
        return None
    def on_key(self, key, scancode, action, mods):
        if key == pg.KEY_SPACE and action == pg.PRESS:
            if self.dy == 0:
                self.dy = 2.0
    def update(self, t, dt):
        # p = abs((t * 0.01) % 2 - 1) / 1.0
        # a = (-920, 2000, -7760)
        # b = (895, 2000, 7530)
        # x, y, z = pg.interpolate(a, b, p)
        # self.wasd.look_at((x, y, z), (x, 0, z))
        # self.wasd.rx = atan2(b[2] - a[2], b[0] - a[0])
        # return
        self.dy = max(self.dy - dt * 2.5, -25.0)
        # self.wasd.y += self.dy
        h = self.get_height()
        if h is None:
            return
        if h < HEIGHT:
            self.dy = 0
            self.wasd.y -= h - HEIGHT
    def draw(self):
        self.window.clear()
        matrix = self.wasd.get_matrix()
        matrix = matrix.perspective(65, self.window.aspect, 1, 100000)
        self.context.matrix = matrix
        self.context.camera_position = self.wasd.position
        self.context.draw()
        # w, h = self.window.size
        # self.font.render('%.1f fps' % self.window.fps, (w - 5, 0), (1, 0))
        # text = 'x=%.2f, y=%.2f, z=%.2f' % self.wasd.position
        # self.font.render(text, (5, 0))

class Window(pg.Window):
    def setup(self):
        self.set_clear_color(0.74, 0.70, 0.64)
        self.set_scene(LoadingScene(self))

class Program(pg.Program):
    VS = '''
    #version 120

    uniform mat4 matrix;
    uniform mat4 model_matrix;
    uniform vec2 uv0;
    uniform vec2 uv1;

    attribute vec4 position;

    varying vec3 frag_position;
    varying vec2 frag_uv;

    void main() {
        gl_Position = matrix * position;
        frag_position = vec3(model_matrix * position);
        float u = (position.x - uv0.x) / (uv1.x - uv0.x);
        float v = 1.0 - (position.z - uv0.y) / (uv1.y - uv0.y);
        frag_uv = vec2(u, v);
    }
    '''
    FS = '''
    #version 120

    uniform sampler2D sampler;
    uniform sampler2D normal_sampler;
    uniform vec3 camera_position;

    uniform mat4 normal_matrix;
    uniform vec3 light_direction;
    uniform vec3 ambient_color;
    uniform vec3 light_color;
    uniform vec3 fog_color;
    uniform float fog_distance;
    uniform float specular_power;
    uniform float specular_multiplier;

    varying vec3 frag_position;
    varying vec2 frag_uv;

    void main() {
        vec3 norm = vec3(texture2D(normal_sampler, frag_uv));
        norm = norm * vec3(2.0) - vec3(1.0);
        norm = norm.yzx;
        vec3 color1 = vec3(0.47, 0.31, 0.24) * 0.8;
        vec3 color2 = vec3(0.82, 0.56, 0.39) * 1.4;
        float pct = vec3(texture2D(sampler, frag_uv)).r;
        vec3 color = mix(color1, color2, pct);
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
        color = min(color * light, vec3(1.0));
        float camera_distance = distance(camera_position, frag_position);
        float fog_factor = pow(min(camera_distance / fog_distance, 1.0), 4.0);
        color = mix(color, fog_color, fog_factor);
        gl_FragColor = vec4(color, 1.0);
    }
    '''
    def __init__(self):
        super(Program, self).__init__(self.VS, self.FS)
    def set_defaults(self, context):
        context.model_matrix = pg.Matrix()
        context.normal_matrix = pg.Matrix().inverse().transpose()
        context.specular_power = 32.0
        context.specular_multiplier = 0.2
        context.ambient_color = (0.4, 0.4, 0.4)
        context.light_color = (0.8, 0.8, 0.8)
        context.fog_color = (0.74, 0.70, 0.64)
        context.fog_distance = 6000
        context.light_direction = pg.normalize((-1, 0.5, 1))

if __name__ == "__main__":
    pg.run(Window)
