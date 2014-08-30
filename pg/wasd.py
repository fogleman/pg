from math import sin, cos, pi, atan2, asin
from .core import Scene
from .matrix import Matrix
from .util import normalize
from . import glfw

class WASD(object):
    def __init__(self, scene_or_window,
        speed=1.0, sensitivity=2.5, invert=False, exclusive=True):
        self.window = scene_or_window
        if isinstance(scene_or_window, Scene):
            self.window = scene_or_window.window
        self.speed = speed
        self.sensitivity = sensitivity
        self.invert = invert
        self.exclusive = exclusive
        self.x = 0
        self.y = 0
        self.z = 0
        self.rx = 0
        self.ry = 0
        self.mx = 0
        self.my = 0
        self.discard = True
        if self.exclusive:
            self.window.set_exclusive()
        scene_or_window.listeners.append(self)
    @property
    def position(self):
        return (self.x, self.y, self.z)
    def look_at(self, position, target):
        px, py, pz = position
        tx, ty, tz = target
        dx, dy, dz = normalize((tx - px, ty - py, tz - pz))
        self.x = px
        self.y = py
        self.z = pz
        self.rx = 2 * pi - (atan2(dx, dz) + pi)
        self.ry = asin(dy)
    def enter(self):
        self.discard = True
    def on_mouse_button(self, button, action, mods):
        if self.exclusive and not self.window.exclusive:
            if button == glfw.MOUSE_BUTTON_1 and action == glfw.PRESS:
                self.window.set_exclusive()
                self.discard = True
                return True
    def on_key(self, key, scancode, action, mods):
        if self.exclusive:
            if key == glfw.KEY_ESCAPE:
                self.window.set_exclusive(False)
    def on_cursor_pos(self, mx, my):
        if self.exclusive and not self.window.exclusive:
            return
        if self.discard:
            self.mx = mx
            self.my = my
            self.discard = False
            return
        m = self.sensitivity / 1000.0
        self.rx += (mx - self.mx) * m
        if self.invert:
            self.ry += (my - self.my) * m
        else:
            self.ry -= (my - self.my) * m
        if self.rx < 0:
            self.rx += 2 * pi
        if self.rx >= 2 * pi:
            self.rx -= 2 * pi
        self.ry = max(self.ry, -pi / 2)
        self.ry = min(self.ry, pi / 2)
        self.mx = mx
        self.my = my
    def get_strafe(self):
        sx = sz = 0
        if glfw.get_key(self.window.handle, ord('W')):
            sz -= 1
        if glfw.get_key(self.window.handle, ord('S')):
            sz += 1
        if glfw.get_key(self.window.handle, ord('A')):
            sx -= 1
        if glfw.get_key(self.window.handle, ord('D')):
            sx += 1
        return (sx, sz)
    def get_matrix(self, matrix=None, translate=True):
        matrix = matrix or Matrix()
        if translate:
            matrix = matrix.translate((-self.x, -self.y, -self.z))
        matrix = matrix.rotate((cos(self.rx), 0, sin(self.rx)), self.ry)
        matrix = matrix.rotate((0, 1, 0), -self.rx)
        return matrix
    def get_sight_vector(self):
        m = cos(self.ry)
        vx = cos(self.rx - pi / 2) * m
        vy = sin(self.ry)
        vz = sin(self.rx - pi / 2) * m
        return (vx, vy, vz)
    def get_motion_vector(self):
        sx, sz = self.get_strafe()
        if sx == 0 and sz == 0:
            return (0, 0, 0)
        strafe = atan2(sz, sx)
        m = cos(self.ry)
        y = sin(self.ry)
        if sx:
            if not sz:
                y = 0
            m = 1
        if sz > 0:
            y = -y
        vx = cos(self.rx + strafe) * m
        vy = y
        vz = sin(self.rx + strafe) * m
        return normalize((vx, vy, vz))
    def update(self, t, dt):
        vx, vy, vz = self.get_motion_vector()
        self.x += vx * self.speed * dt
        self.y += vy * self.speed * dt
        self.z += vz * self.speed * dt
