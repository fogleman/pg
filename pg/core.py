from ctypes import *
from OpenGL.GL import *
from PIL import Image
from math import sin, cos, pi, atan2
from matrix import Matrix
from util import normalize
import glfw
import os
import time

FLOATS = set([
    GL_FLOAT,
    GL_FLOAT_VEC2,
    GL_FLOAT_VEC3,
    GL_FLOAT_VEC4,
])

INTS = set([
    GL_INT,
    GL_INT_VEC2,
    GL_INT_VEC3,
    GL_INT_VEC4,
])

BOOLS = set([
    GL_BOOL,
    GL_BOOL_VEC2,
    GL_BOOL_VEC3,
    GL_BOOL_VEC4,
])

MATRICES = set([
    GL_FLOAT_MAT2,
    GL_FLOAT_MAT3,
    GL_FLOAT_MAT4,
])

SAMPLERS = set([
    GL_SAMPLER_2D,
    GL_SAMPLER_CUBE,
])

TEXTURES = [
    GL_TEXTURE0,
    GL_TEXTURE1,
    GL_TEXTURE2,
    GL_TEXTURE3,
    GL_TEXTURE4,
    GL_TEXTURE5,
    GL_TEXTURE6,
    GL_TEXTURE7,
    GL_TEXTURE8,
    GL_TEXTURE9,
    GL_TEXTURE10,
    GL_TEXTURE11,
    GL_TEXTURE12,
    GL_TEXTURE13,
    GL_TEXTURE14,
    GL_TEXTURE15,
    GL_TEXTURE16,
    GL_TEXTURE17,
    GL_TEXTURE18,
    GL_TEXTURE19,
    GL_TEXTURE20,
    GL_TEXTURE21,
    GL_TEXTURE22,
    GL_TEXTURE23,
    GL_TEXTURE24,
    GL_TEXTURE25,
    GL_TEXTURE26,
    GL_TEXTURE27,
    GL_TEXTURE28,
    GL_TEXTURE29,
    GL_TEXTURE30,
    GL_TEXTURE31,
]

class Shader(object):
    def __init__(self, shader_type, shader_source):
        if os.path.exists(shader_source):
            with open(shader_source, 'r') as fp:
                shader_source = fp.read()
        self.handle = glCreateShader(shader_type)
        glShaderSource(self.handle, shader_source)
        glCompileShader(self.handle)
        log = glGetShaderInfoLog(self.handle)
        if log:
            raise Exception(log)

class VertexShader(Shader):
    def __init__(self, shader_source):
        super(VertexShader, self).__init__(GL_VERTEX_SHADER, shader_source)

class FragmentShader(Shader):
    def __init__(self, shader_source):
        super(FragmentShader, self).__init__(GL_FRAGMENT_SHADER, shader_source)

class VertexBuffer(object):
    def __init__(self, components, data):
        self.components = components
        self.count = len(data) / components
        handle = c_uint()
        glGenBuffers(1, byref(handle))
        self.handle = handle.value
        glBindBuffer(GL_ARRAY_BUFFER, self.handle)
        glBufferData(
            GL_ARRAY_BUFFER, sizeof(c_float) * len(data),
            (c_float * len(data))(*data), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
    def slice(self, components, offset):
        return VertexBufferSlice(self, components, offset)
    def set(self, location):
        glEnableVertexAttribArray(location)
        glBindBuffer(GL_ARRAY_BUFFER, self.handle)
        glVertexAttribPointer(
            location, self.components, GL_FLOAT, GL_FALSE, 0, c_void_p())

class VertexBufferSlice(object):
    def __init__(self, parent, components, offset):
        self.parent = parent
        self.components = components
        self.offset = offset
        self.count = self.parent.count
    def set(self, location):
        glEnableVertexAttribArray(location)
        glBindBuffer(GL_ARRAY_BUFFER, self.parent.handle)
        glVertexAttribPointer(
            location, self.components, GL_FLOAT, GL_FALSE,
            sizeof(c_float) * self.parent.components,
            c_void_p(sizeof(c_float) * self.offset))

class Texture(object):
    def __init__(self, index, path):
        self.index = index
        im = Image.open(path).convert('RGBA')
        width, height = im.size
        data = im.tobytes()
        handle = c_uint()
        glGenTextures(1, byref(handle))
        self.handle = handle.value
        glActiveTexture(TEXTURES[index])
        glBindTexture(GL_TEXTURE_2D, self.handle)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,
            GL_UNSIGNED_BYTE, data)

class Attribute(object):
    def __init__(self, location, name, size, data_type):
        self.location = location
        self.name = name
        self.size = size
        self.data_type = data_type
    def set(self, value):
        value.set(self.location)
    def __repr__(self):
        return 'Attribute%s' % str(
            (self.location, self.name, self.size, self.data_type))

class Uniform(object):
    def __init__(self, location, name, size, data_type):
        self.location = location
        self.name = name
        self.size = size
        self.data_type = data_type
    def set(self, value):
        if isinstance(value, Matrix):
            value = value.value
        elif isinstance(value, Texture):
            value = value.index
        try:
            count = len(value)
        except Exception:
            value = [value]
            count = 1
        if self.data_type in MATRICES:
            funcs = {
                4: glUniformMatrix2fv,
                9: glUniformMatrix3fv,
                16: glUniformMatrix4fv,
            }
            funcs[count](self.location, 1, False, (c_float * count)(*value))
        elif self.data_type in FLOATS:
            funcs = {
                1: glUniform1f,
                2: glUniform2f,
                3: glUniform3f,
                4: glUniform4f,
            }
            funcs[count](self.location, *value)
        elif self.data_type in INTS or self.data_type in BOOLS:
            funcs = {
                1: glUniform1i,
                2: glUniform2i,
                3: glUniform3i,
                4: glUniform4i,
            }
            funcs[count](self.location, *value)
        elif self.data_type in SAMPLERS:
            glUniform1i(self.location, *value)
    def __repr__(self):
        return 'Uniform%s' % str(
            (self.location, self.name, self.size, self.data_type))

class Program(object):
    def __init__(self, vs, fs):
        if not isinstance(vs, Shader):
            vs = VertexShader(vs)
        if not isinstance(fs, Shader):
            fs = FragmentShader(fs)
        self.vs = vs
        self.fs = fs
        self.handle = glCreateProgram()
        glAttachShader(self.handle, self.vs.handle)
        glAttachShader(self.handle, self.fs.handle)
        glLinkProgram(self.handle)
        log = glGetProgramInfoLog(self.handle)
        if log:
            raise Exception(log)
    def use(self):
        glUseProgram(self.handle)
    def get_attributes(self):
        result = []
        count = c_int()
        glGetProgramiv(self.handle, GL_ACTIVE_ATTRIBUTES, byref(count))
        name = create_string_buffer(256)
        size = c_int()
        data_type = c_int()
        for index in xrange(count.value):
            glGetActiveAttrib(
                self.handle, index, 256, None,
                byref(size), byref(data_type), name)
            location = glGetAttribLocation(self.handle, name.value)
            attribute = Attribute(
                location, name.value, size.value, data_type.value)
            result.append(attribute)
        return result
    def get_uniforms(self):
        result = []
        count = c_int()
        glGetProgramiv(self.handle, GL_ACTIVE_UNIFORMS, byref(count))
        for index in xrange(count.value):
            name, size, data_type = glGetActiveUniform(self.handle, index)
            location = glGetUniformLocation(self.handle, name)
            uniform = Uniform(location, name, size, data_type)
            result.append(uniform)
        return result

class Context(object):
    def __init__(self, program):
        self._program = program
        self._attributes = dict((x.name, x) for x in program.get_attributes())
        self._uniforms = dict((x.name, x) for x in program.get_uniforms())
        self._attribute_values = {}
        self._uniform_values = {}
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super(Context, self).__setattr__(name, value)
        elif name in self._attributes:
            self._attribute_values[name] = value
        elif name in self._uniforms:
            self._uniform_values[name] = value
        else:
            super(Context, self).__setattr__(name, value)
    def draw(self, mode):
        self._program.use()
        for name, value in self._uniform_values.iteritems():
            self._uniforms[name].set(value)
        for name, value in self._attribute_values.iteritems():
            self._attributes[name].set(value)
        count = min(x.count for x in self._attribute_values.itervalues())
        glDrawArrays(mode, 0, count)

class WASD(object):
    # TODO: set position
    # TODO: set sight vector
    def __init__(self, window,
        speed=1.0, sensitivity=2.5, invert=False, exclusive=True):
        self.window = window
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
        if self.exclusive:
            self.window.set_exclusive()
        self.window.listeners.append(self)
    def on_mouse_button(self, button, action, mods):
        if self.exclusive:
            if button == glfw.MOUSE_BUTTON_1 and action == glfw.PRESS:
                self.window.set_exclusive()
    def on_key(self, key, scancode, action, mods):
        if self.exclusive:
            if key == glfw.KEY_ESCAPE:
                self.window.set_exclusive(False)
    def on_cursor_pos(self, mx, my):
        if self.exclusive and not self.window.exclusive:
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
    def get_matrix(self, matrix=None):
        matrix = matrix or Matrix()
        matrix = matrix.translate((-self.x, -self.y, -self.z))
        matrix = matrix.rotate((cos(self.rx), 0, sin(self.rx)), self.ry)
        matrix = matrix.rotate((0, 1, 0), -self.rx)
        return matrix
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

class App(object):
    instance = None
    def __init__(self):
        if not glfw.init():
            raise Exception
        App.instance = self
        self.windows = []
    def run(self):
        while self.windows:
            glfw.poll_events()
            for window in list(self.windows):
                window.tick()
        glfw.terminate()

class Window(object):
    def __init__(self, size, title='Python Graphics'):
        width, height = size
        self.handle = glfw.create_window(width, height, title, None, None)
        if not self.handle:
            raise Exception
        self.exclusive = False
        self.start = self.time = time.time()
        self.use()
        self.on_size(*size)
        self.listeners = [self]
        self.set_callbacks()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        self.setup()
        App.instance.windows.append(self)
    def set_exclusive(self, exclusive=True):
        if exclusive == self.exclusive:
            return
        self.exclusive = exclusive
        if exclusive:
            glfw.set_input_mode(self.handle, glfw.CURSOR, glfw.CURSOR_DISABLED)
        else:
            glfw.set_input_mode(self.handle, glfw.CURSOR, glfw.CURSOR_NORMAL)
    def setup(self):
        pass
    def update(self, t, dt):
        pass
    def draw(self):
        pass
    def teardown(self):
        pass
    def use(self):
        glfw.make_context_current(self.handle)
    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    def tick(self):
        self.use()
        if glfw.window_should_close(self.handle):
            self.teardown()
            App.instance.windows.remove(self)
            glfw.destroy_window(self.handle)
            return
        now = time.time()
        self.call_listeners('update', now - self.start, now - self.time)
        self.time = now
        self.draw()
        glfw.swap_buffers(self.handle)
    def set_callbacks(self):
        glfw.set_window_size_callback(self.handle, self._on_size)
        glfw.set_cursor_pos_callback(self.handle, self._on_cursor_pos)
        glfw.set_mouse_button_callback(self.handle, self._on_mouse_button)
        glfw.set_key_callback(self.handle, self._on_key)
        glfw.set_char_callback(self.handle, self._on_char)
    def call_listeners(self, name, *args):
        for listener in self.listeners:
            if hasattr(listener, name):
                getattr(listener, name)(*args)
    def _on_size(self, window, width, height):
        self.call_listeners('on_size', width, height)
    def on_size(self, width, height):
        pass
    def _on_cursor_pos(self, window, x, y):
        self.call_listeners('on_cursor_pos', x, y)
    def on_cursor_pos(self, x, y):
        pass
    def _on_mouse_button(self, window, button, action, mods):
        self.call_listeners('on_mouse_button', button, action, mods)
    def on_mouse_button(self, button, action, mods):
        pass
    def _on_key(self, window, key, scancode, action, mods):
        self.call_listeners('on_key', key, scancode, action, mods)
    def on_key(self, key, scancode, action, mods):
        pass
    def _on_char(self, window, codepoint):
        self.call_listeners('on_char', codepoint)
    def on_char(self, codepoint):
        pass
