from ctypes import *
from OpenGL.GL import *
from PIL import Image
from matrix import Matrix
from util import flatten, interleave
import glfw
import os
import time

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
    def __init__(self, data=None):
        self.handle = glGenBuffers(1)
        if data is not None:
            self.set_data(data)
    def set_data(self, data):
        self.vertex_count = len(data)
        self.components = len(data[0]) if self.vertex_count else 1
        self.size = self.vertex_count * self.components
        flat = flatten(data)
        if len(flat) != self.size:
            raise Exception
        glBindBuffer(GL_ARRAY_BUFFER, self.handle)
        glBufferData(
            GL_ARRAY_BUFFER,
            sizeof(c_float) * self.size,
            (c_float * self.size)(*flat),
            GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
    def delete(self):
        glDeleteBuffers(1, self.handle)
    def slice(self, components, offset):
        return VertexBufferSlice(self, components, offset)
    def slices(self, *args):
        offset = 0
        result = []
        for components in args:
            result.append(self.slice(components, offset))
            offset += components
        return result
    def bind(self, location):
        glEnableVertexAttribArray(location)
        glBindBuffer(GL_ARRAY_BUFFER, self.handle)
        glVertexAttribPointer(
            location, self.components, GL_FLOAT, GL_FALSE,
            0, c_void_p())

class VertexBufferSlice(object):
    def __init__(self, parent, components, offset):
        self.parent = parent
        self.vertex_count = self.parent.vertex_count
        self.components = components
        self.offset = offset
    def bind(self, location):
        glEnableVertexAttribArray(location)
        glBindBuffer(GL_ARRAY_BUFFER, self.parent.handle)
        glVertexAttribPointer(
            location, self.components, GL_FLOAT, GL_FALSE,
            sizeof(c_float) * self.parent.components,
            c_void_p(sizeof(c_float) * self.offset))

class IndexBuffer(object):
    def __init__(self, data=None):
        self.handle = glGenBuffers(1)
        if data is not None:
            self.set_data(data)
    def set_data(self, data):
        self.size = len(data)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.handle)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            sizeof(c_uint) * self.size,
            (c_uint * self.size)(*data),
            GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    def delete(self):
        glDeleteBuffers(1, self.handle)

def index(*args):
    sizes = [len(x[0]) for x in args]
    data = interleave(*args)
    distinct = sorted(set(data))
    lookup = dict((x, i) for i, x in enumerate(distinct))
    indices = [lookup[x] for x in data]
    vertex_buffer = VertexBuffer(distinct)
    index_buffer = IndexBuffer(indices)
    return index_buffer, vertex_buffer.slices(*sizes)

class Texture(object):
    UNITS = [
        GL_TEXTURE0, GL_TEXTURE1, GL_TEXTURE2, GL_TEXTURE3,
        GL_TEXTURE4, GL_TEXTURE5, GL_TEXTURE6, GL_TEXTURE7,
        GL_TEXTURE8, GL_TEXTURE9, GL_TEXTURE10, GL_TEXTURE11,
        GL_TEXTURE12, GL_TEXTURE13, GL_TEXTURE14, GL_TEXTURE15,
        GL_TEXTURE16, GL_TEXTURE17, GL_TEXTURE18, GL_TEXTURE19,
        GL_TEXTURE20, GL_TEXTURE21, GL_TEXTURE22, GL_TEXTURE23,
        GL_TEXTURE24, GL_TEXTURE25, GL_TEXTURE26, GL_TEXTURE27,
        GL_TEXTURE28, GL_TEXTURE29, GL_TEXTURE30, GL_TEXTURE31,
    ]
    def __init__(self, unit, im):
        self.unit = unit
        if isinstance(im, basestring):
            im = Image.open(im)
        im = im.convert('RGBA').transpose(Image.FLIP_TOP_BOTTOM)
        width, height = im.size
        data = im.tobytes()
        self.handle = glGenTextures(1)
        glActiveTexture(Texture.UNITS[unit])
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
    def bind(self, value):
        value.bind(self.location)
    def __repr__(self):
        return 'Attribute%s' % str(
            (self.location, self.name, self.size, self.data_type))

class Uniform(object):
    FLOATS = set([GL_FLOAT, GL_FLOAT_VEC2, GL_FLOAT_VEC3, GL_FLOAT_VEC4])
    INTS = set([GL_INT, GL_INT_VEC2, GL_INT_VEC3, GL_INT_VEC4])
    BOOLS = set([GL_BOOL, GL_BOOL_VEC2, GL_BOOL_VEC3, GL_BOOL_VEC4])
    MATS = set([GL_FLOAT_MAT2, GL_FLOAT_MAT3, GL_FLOAT_MAT4])
    SAMPLERS = set([GL_SAMPLER_2D, GL_SAMPLER_CUBE])
    def __init__(self, location, name, size, data_type):
        self.location = location
        self.name = name
        self.size = size
        self.data_type = data_type
    def bind(self, value):
        if isinstance(value, Matrix):
            value = value.value
        elif isinstance(value, Texture):
            value = value.unit
        try:
            count = len(value)
        except Exception:
            value = [value]
            count = 1
        if self.data_type in Uniform.MATS:
            funcs = {
                4: glUniformMatrix2fv,
                9: glUniformMatrix3fv,
                16: glUniformMatrix4fv,
            }
            funcs[count](self.location, 1, False, (c_float * count)(*value))
        elif self.data_type in Uniform.FLOATS:
            funcs = {
                1: glUniform1f,
                2: glUniform2f,
                3: glUniform3f,
                4: glUniform4f,
            }
            funcs[count](self.location, *value)
        elif self.data_type in Uniform.INTS or self.data_type in Uniform.BOOLS:
            funcs = {
                1: glUniform1i,
                2: glUniform2i,
                3: glUniform3i,
                4: glUniform4i,
            }
            funcs[count](self.location, *value)
        elif self.data_type in Uniform.SAMPLERS:
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
    def set_defaults(self, context):
        pass
    def get_attributes(self):
        result = []
        count = glGetProgramiv(self.handle, GL_ACTIVE_ATTRIBUTES)
        name = create_string_buffer(256)
        size = c_int()
        data_type = c_int()
        for index in xrange(count):
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
        count = glGetProgramiv(self.handle, GL_ACTIVE_UNIFORMS)
        for index in xrange(count):
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
        self._dirty = set()
        self._program.set_defaults(self)
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super(Context, self).__setattr__(name, value)
        elif name in self._attributes:
            self._attribute_values[name] = value
        elif name in self._uniforms:
            self._uniform_values[name] = value
            self._dirty.add(name)
        else:
            super(Context, self).__setattr__(name, value)
    def __getattr__(self, name):
        if name.startswith('_'):
            super(Context, self).__getattr__(name)
        elif name in self._attributes:
            return self._attribute_values[name]
        elif name in self._uniforms:
            return self._uniform_values[name]
        else:
            super(Context, self).__getattr__(name)
    def prepare(self):
        self._program.use()
        for name, value in self._uniform_values.iteritems():
            if name in self._dirty:
                self._uniforms[name].bind(value)
        for name, value in self._attribute_values.iteritems():
            self._attributes[name].bind(value)
        self._dirty.clear()
    def draw(self, mode):
        self.prepare()
        vertex_count = min(
            x.vertex_count for x in self._attribute_values.itervalues())
        glDrawArrays(mode, 0, vertex_count)
    def draw_elements(self, mode, index_buffer):
        self.prepare()
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, index_buffer.handle)
        glDrawElements(mode, index_buffer.size, GL_UNSIGNED_INT, c_void_p())
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

class App(object):
    instance = None
    def __init__(self):
        if not glfw.init():
            raise Exception
        App.instance = self
        self.windows = []
    def run(self):
        while self.windows:
            self.tick()
        glfw.terminate()
    def tick(self):
        glfw.poll_events()
        for window in list(self.windows):
            window.tick()

class FPS(object):
    def __init__(self):
        self.time = time.time()
        self.counter = 0
        self.value = 0
    def tick(self):
        self.counter += 1
        now = time.time()
        elapsed = now - self.time
        if elapsed >= 1:
            self.value = self.counter / elapsed
            self.counter = 0
            self.time = now

class Window(object):
    def __init__(self, size=(800, 600), title='Python Graphics'):
        self.size = width, height = size
        self.handle = glfw.create_window(width, height, title, None, None)
        if not self.handle:
            raise Exception
        self.use()
        self.configure()
        self.aspect = float(width) / height
        self.exclusive = False
        self.start = self.time = time.time()
        self._fps = FPS()
        self.listeners = [self]
        self.set_callbacks()
        self.call('setup')
        App.instance.windows.append(self)
    @property
    def t(self):
        return time.time() - self.start
    @property
    def fps(self):
        return self._fps.value
    def configure(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    def close(self):
        glfw.set_window_should_close(self.handle, 1)
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
    def clear_color_buffer(self):
        glClear(GL_COLOR_BUFFER_BIT)
    def clear_depth_buffer(self):
        glClear(GL_DEPTH_BUFFER_BIT)
    def tick(self):
        self._fps.tick()
        self.use()
        if glfw.window_should_close(self.handle):
            self.call('teardown')
            App.instance.windows.remove(self)
            glfw.destroy_window(self.handle)
            return
        now = time.time()
        self.call('update', now - self.start, now - self.time)
        self.time = now
        self.call('draw')
        glfw.swap_buffers(self.handle)
    def save_image(self, path):
        width, height = self.size
        data = (c_ubyte * (width * height * 3))()
        glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE, data)
        im = Image.frombytes('RGB', (width, height), data)
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
        im.save(path)
    def set_callbacks(self):
        glfw.set_window_size_callback(self.handle, self._on_size)
        glfw.set_cursor_pos_callback(self.handle, self._on_cursor_pos)
        glfw.set_mouse_button_callback(self.handle, self._on_mouse_button)
        glfw.set_key_callback(self.handle, self._on_key)
        glfw.set_char_callback(self.handle, self._on_char)
    def call(self, name, *args, **kwargs):
        for listener in self.listeners:
            if hasattr(listener, name):
                getattr(listener, name)(*args, **kwargs)
    def _on_size(self, window, width, height):
        self.size = (width, height)
        self.aspect = float(width) / height
        self.call('on_size', width, height)
    def on_size(self, width, height):
        pass
    def _on_cursor_pos(self, window, x, y):
        self.call('on_cursor_pos', x, y)
    def on_cursor_pos(self, x, y):
        pass
    def _on_mouse_button(self, window, button, action, mods):
        self.call('on_mouse_button', button, action, mods)
    def on_mouse_button(self, button, action, mods):
        pass
    def _on_key(self, window, key, scancode, action, mods):
        self.call('on_key', key, scancode, action, mods)
    def on_key(self, key, scancode, action, mods):
        pass
    def _on_char(self, window, codepoint):
        self.call('on_char', codepoint)
    def on_char(self, codepoint):
        pass
