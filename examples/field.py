from math import pi, sin, cos
import pg
import random

SCALE = 512
PARTICLE_COUNT = 13

def points(sides, radius, rotation):
    rotation = rotation - pi / 2
    angle = 2 * pi / sides
    angles = [angle * i + rotation for i in range(sides)]
    return [(cos(a) * radius, sin(a) * radius, 1.0) for a in angles]

class Window(pg.Window):
    def setup(self):
        plane = pg.Plane((0, 0, 0), (0, 0, 1), 1)
        self.context = pg.Context(Program())
        self.context.position = pg.VertexBuffer(plane.positions)
        self.context.matrix = pg.Matrix().orthographic(-1, 1, -1, 1, -1, 1)
    def update(self, t, dt):
        t0 = t / 24
        t1 = t0
        t2 = -t0 * pi
        r1 = SCALE
        r2 = SCALE / 2
        m = sin(t0 * pi / 2) * 2
        particles = [(0, 0, m)] + points(6, r1, t1) + points(6, r2, t2)
        self.context.particles = particles
        self.context.t = t0
    def draw(self):
        self.clear()
        self.context.w, self.context.h = self.framebuffer_size
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
    uniform float t;
    uniform vec3 particles[%d];

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
    const float pi = 3.141592653589793;

    vec4 compute(vec2 c) {
        float dx = 0;
        float dy = 0;
        for (int i = 0; i < %d; i++) {
            vec3 p = particles[i];
            float d = distance(p.xy, c);
            float a = atan(c.y - p.y, c.x - p.x);
            dx += p.z * cos(a) / d;
            dy += p.z * sin(a) / d;
        }
        float d = length(vec2(dx, dy));
        float n = log(d) / log(2.0 + sin(t) * 0.8);
        float f = mod(n, 1.0);
        if (f < 0.5) {
            return background;
        }
        else {
            float e = (abs(f - 0.75) - 0.25) * 4;
            int index = int(mod(n, palette.length()));
            float pct = clamp(pow(e, 0.3), 0, 1);
            return mix(background, palette[index], pct);
        }
    }

    void main() {
        vec2 c = gl_FragCoord.xy - vec2(w / 2.0, h / 2.0);
        gl_FragColor = compute(c);
    }
    ''' % (PARTICLE_COUNT, PARTICLE_COUNT)

def main():
    app = pg.App()
    Window((1000, 1000))
    app.run()

if __name__ == "__main__":
    main()
