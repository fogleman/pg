from OpenGL.GL import *
from core import Context, Texture, VertexBuffer
from itertools import product
from math import ceil, log
from matrix import Matrix
from PIL import Image, ImageDraw, ImageFont
from programs import TextProgram
from util import interleave

class Font(object):
    def __init__(self, unit, name, size):
        self.load(name, size)
        self.context = Context(TextProgram())
        self.context.sampler = Texture(unit, self.im)
    def render(self, text, window_size, coord=(0, 0), anchor=(0, 0)):
        size, position, uv = self.compute_vertex_data(text)
        ww, wh = window_size
        tx, ty = coord
        ax, ay = anchor
        tw, th = size
        matrix = Matrix()
        matrix = matrix.translate((tx - tw * ax, ty - th * ay, 0))
        matrix = matrix.orthographic(0, ww, wh, 0, -1, 1)
        self.context.matrix = matrix
        vertex_buffer = VertexBuffer(interleave(position, uv))
        self.context.position, self.context.uv = vertex_buffer.slices(2, 2)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.context.draw(GL_TRIANGLES)
        glDisable(GL_BLEND)
        vertex_buffer.delete()
    def compute_vertex_data(self, text):
        position = []
        uv = []
        data = [
            (0, 0), (0, 1), (1, 0),
            (0, 1), (1, 1), (1, 0),
        ]
        x = y = 0
        previous = None
        for c in text:
            if c not in self.sizes:
                c = ' '
            index = ord(c) - 32
            row = index / 10
            col = index % 10
            u = self.du * col
            v = self.dv * row
            sx, sy = self.sizes[c]
            ox, oy = self.offsets[c]
            k = self.kerning.get((previous, c), 0)
            x += k
            for i, j in data:
                position.append((x + i * self.dx + ox, y + j * self.dy + oy))
                uv.append((u + i * self.du, 1.0 - v - j * self.dv))
            x += ox + sx
            previous = c
        size = (x, self.dy)
        return size, position, uv
    def load(self, name, size):
        font = ImageFont.truetype(name, size)
        chars = [chr(x) for x in range(32, 127)]
        sizes = dict((c, font.getsize(c)) for c in chars)
        offsets = dict((c, font.getoffset(c)) for c in chars)
        kerning = {}
        for c1, c2 in product(chars, repeat=2):
            a = sizes[c1][0] + sizes[c2][0]
            b = font.getsize(c1 + c2)[0]
            kerning[(c1, c2)] = b - a
        mw = max(sizes[c][0] for c in chars) + 1
        mh = max(sizes[c][1] for c in chars) + 1
        rows = 10
        cols = 10
        w = mw * cols
        h = mh * rows
        w = int(2 ** ceil(log(w) / log(2)))
        h = int(2 ** ceil(log(h) / log(2)))
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        for (row, col), c in zip(product(range(rows), range(cols)), chars):
            x = col * mw
            y = row * mh
            dx, dy = offsets[c]
            # draw.rectangle((x, y, x + mw, y + mh), outline=(48, 48, 48, 255))
            draw.text((x + 1 - dx, y + 1 - dy), c, (255, 255, 255, 255), font)
        self.dx = mw
        self.dy = mh
        self.du = float(mw) / w
        self.dv = float(mh) / h
        self.sizes = sizes
        self.offsets = offsets
        self.kerning = kerning
        self.im = im
