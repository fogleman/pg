from math import pi, sin
import pg

SCALE = 256
MIN_CIRCLE_SIZE = SCALE / 2
MAX_CIRCLE_SIZE = SCALE * 2
CIRCLE_SPACING = SCALE * 1
GRID_SIZE = 7
SPEED = 1.0 / 10
OFFSET_MULTIPLIER = 2.0
CIRCLE_COUNT = GRID_SIZE * GRID_SIZE

class Window(pg.Window):
    def setup(self):
        plane = pg.Plane((0, 0, 0), (0, 0, 1), 1)
        self.context = pg.Context(Program())
        self.context.position = pg.VertexBuffer(plane.positions)
        self.context.matrix = pg.Matrix().orthographic(-1, 1, -1, 1, -1, 1)
        self.positions = []
        n = GRID_SIZE
        m = CIRCLE_SPACING
        for i in range(n):
            for j in range(n):
                x = (i - (n - 1) / 2.0) * m
                y = (j - (n - 1) / 2.0) * m
                d = (x * x + y * y) ** 0.5
                self.positions.append((x, y, d))
        self.max_distance = max(x[-1] for x in self.positions)
    def circles(self):
        result = []
        for x, y, d in self.positions:
            t = d / self.max_distance * pi * OFFSET_MULTIPLIER
            p = (sin(t - self.t * 2 * pi * SPEED) + 1) / 2
            r = MIN_CIRCLE_SIZE + p * (MAX_CIRCLE_SIZE - MIN_CIRCLE_SIZE)
            result.append((x, y, r))
        return result
    def draw(self):
        self.clear()
        self.context.w, self.context.h = self.framebuffer_size
        self.context.circles = self.circles()
        self.context.draw()

class Program(pg.BaseProgram):
    VS = '''
    #version 120

    uniform mat4 matrix;
    attribute vec4 position;

    void main() {
        gl_Position = matrix * position;
    }
    '''
    FS = '''
    #version 120

    uniform float w;
    uniform float h;
    uniform vec3 circles[%d];

    const vec4 palette[10] = vec4[10](
        vec4(0.122, 0.467, 0.706, 1.0),
        vec4(1.000, 0.498, 0.055, 1.0),
        vec4(0.173, 0.627, 0.173, 1.0),
        vec4(0.839, 0.153, 0.157, 1.0),
        vec4(0.580, 0.404, 0.741, 1.0),
        vec4(0.549, 0.337, 0.294, 1.0),
        vec4(0.890, 0.467, 0.761, 1.0),
        vec4(0.498, 0.498, 0.498, 1.0),
        vec4(0.737, 0.741, 0.133, 1.0),
        vec4(0.090, 0.745, 0.812, 1.0)
    );

    const vec4 background = vec4(0, 0, 0, 1);

    void main() {
        int count = 0;
        float e = 1e9;
        vec2 p = gl_FragCoord.xy - vec2(w / 2.0, h / 2.0);
        for (int i = 0; i < %d; i++) {
            vec2 c = circles[i].xy;
            float r = circles[i].z;
            float d = distance(p, c);
            e = min(e, abs(d - r));
            if (d <= r) {
                count++;
            }
        }
        if (mod(count, 2) == 0) {
            gl_FragColor = background;
        }
        else {
            vec4 color = palette[int(mod(count / 2, palette.length()))];
            float pct = clamp(pow(e / 2, 2), 0, 1);
            gl_FragColor = mix(background, color, pct);
        }
    }
    ''' % (CIRCLE_COUNT, CIRCLE_COUNT)

def main():
    app = pg.App()
    Window((1000, 1000))
    app.run()

if __name__ == "__main__":
    main()
