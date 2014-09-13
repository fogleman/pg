from .core import VertexBuffer, Texture
from .pack import pack
from .matrix import Matrix
from .util import interleave
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
    def generate_vertex_data(self):
        data = [
            (0, 0), (1, 0), (0, 1),
            (1, 0), (1, 1), (0, 1),
        ]
        ax, ay = self.anchor
        px, py = self.position
        w, h = self.frame.size
        s = self.scale
        coords = self.frame.coords
        u = (coords[0], coords[2])
        v = (coords[1], coords[3])
        position = [(x - ax, y - ay) for x, y in data]
        matrix = Matrix()
        matrix = matrix.scale((w * s, h * s, 1))
        matrix = matrix.rotate((0, 0, -1), self.rotation)
        matrix = matrix.translate((px, py, 0))
        position = [matrix * x for x in position]
        uv = []
        for i, j in data:
            uv.append((u[i], v[j]))
        return position, uv
    def draw(self, context):
        # TODO: batched drawing
        position, uv = self.generate_vertex_data()
        vertex_buffer = VertexBuffer(interleave(position, uv))
        context.position, context.uv = vertex_buffer.slices(2, 2)
        glEnable(GL_BLEND)
        glDisable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        context.draw()
        glEnable(GL_DEPTH_TEST)
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
            v1 = 1 - (y + p) / float(th - 1)
            v2 = 1 - (y + h - p) / float(th - 1)
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
