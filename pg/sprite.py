from .core import VertexBuffer, Texture
from .pack import pack
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
        z = self.z
        coords = self.frame.coords
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        position = []
        for i, j in points:
            x, y = (i - ax) * fw, (j - ay) * fh
            x, y = px + x * rc - y * rs, py + x * rs + y * rc
            position.append((x, y, z))
        uv = [
            (coords[0], coords[1]),
            (coords[2], coords[1]),
            (coords[0], coords[3]),
            (coords[2], coords[3]),
        ]
        indexes = [0, 1, 2, 1, 3, 2]
        position = [position[i] for i in indexes]
        uv = [uv[i] for i in indexes]
        return position, uv
    def draw(self, context):
        # TODO: batched drawing
        position, uv = self.generate_vertex_data()
        vertex_buffer = VertexBuffer(interleave(position, uv))
        context.position, context.uv = vertex_buffer.slices(3, 2)
        glEnable(GL_BLEND)
        # glDisable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        context.draw()
        # glEnable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)
        vertex_buffer.delete()

class SpriteFrame(object):
    def __init__(self, name, size, coords):
        self.name = name
        self.size = size
        self.coords = coords
    def __call__(self):
        return Sprite(self)

class SpriteSheet(object):
    def __init__(self, arg):
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
        self.im = im
    def __getattr__(self, name):
        if name in self.lookup:
            return self.lookup[name]
        return super(SpriteSheet, self).__getattr__(name)
    def __getitem__(self, name):
        return self.lookup[name]
    def texture(self, unit):
        return Texture(unit, self.im)
