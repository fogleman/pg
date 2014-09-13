from .core import VertexBuffer, Texture, Context
from .pack import pack
from .programs import TextureProgram
from .util import interleave
from math import sin, cos
from OpenGL.GL import *
from PIL import Image
import os

def load_directory(path):
    names = []
    images = []
    extensions = set(['.png', '.jpg'])
    for name in os.listdir(path):
        base, ext = os.path.splitext(name)
        if ext.lower() not in extensions:
            continue
        im = Image.open(os.path.join(path, name))
        names.append(base)
        images.append(im)
    return names, images

def load_images(paths):
    names = []
    images = []
    for path in paths:
        base, ext = os.path.splitext(path)
        im = Image.open(path)
        names.append(base)
        images.append(im)
    return names, images

class SpriteBatch(object):
    def __init__(self, sheet):
        self.sprites = []
        self.context = Context(TextureProgram())
        self.context.sampler = sheet

class Sprite(object):
    def __init__(self, frame):
        self.frame = frame
        self.anchor = (0.5, 0.5)
        self.position = (0, 0)
        self.rotation = 0
        self.scale = 1
        self.z = 0
    def generate_vertex_data(self):
        ax, ay = self.anchor
        px, py = self.position
        fw, fh = self.frame.size
        rs = sin(self.rotation)
        rc = cos(self.rotation)
        s = self.scale
        z = self.z
        coords = self.frame.coords
        u = (coords[0], coords[2])
        v = (coords[1], coords[3])
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        data = []
        for i, j in points:
            x, y = (i - ax) * fw * s, (j - ay) * fh * s
            x, y = px + x * rc - y * rs, py + x * rs + y * rc
            data.append((x, y, z, u[i], v[j]))
        indexes = [0, 1, 2, 1, 3, 2]
        return [data[i] for i in indexes]
    def draw(self, context):
        # TODO: batched drawing
        vb = VertexBuffer(self.generate_vertex_data())
        context.position, context.uv = vb.slices(3, 2)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        context.draw()
        glDisable(GL_BLEND)
        vb.delete()

class SpriteFrame(object):
    def __init__(self, name, size, coords):
        self.name = name
        self.size = size
        self.coords = coords
    def __call__(self):
        return Sprite(self)

class SpriteSheet(object):
    def __init__(self, unit, arg):
        if os.path.isdir(arg):
            names, images = load_directory(arg)
        else:
            names, images = load_images(arg)
        p = 1
        sizes = [x.size for x in images]
        sizes = [(w + p * 2, h + p * 2) for w, h in sizes]
        size, positions = pack(sizes)
        im = Image.new('RGBA', size)
        tw, th = size
        self.lookup = {}
        for name, image, (x, y, w, h) in zip(names, images, positions):
            u1 = (x + p) / float(tw - 1)
            u2 = (x + w - p) / float(tw - 1)
            v2 = 1 - (y + p) / float(th - 1)
            v1 = 1 - (y + h - p) / float(th - 1)
            im.paste(image, (x + p, y + p))
            frame = SpriteFrame(name, (w, h), (u1, v1, u2, v2))
            self.lookup[name] = frame
        self.texture = Texture(unit, im)
    def get_uniform_value(self):
        return self.texture.unit
    def __getattr__(self, name):
        if name in self.lookup:
            return self.lookup[name]
        return super(SpriteSheet, self).__getattr__(name)
    def __getitem__(self, name):
        return self.lookup[name]
