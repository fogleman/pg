from OpenGL.GL import *
from itertools import product
from math import ceil, log
from PIL import Image, ImageDraw, ImageFont
from .core import Context, Texture, VertexBuffer, Scene
from .matrix import Matrix
from .programs import TextProgram
from .util import interleave

def float_to_byte_color(color):
    return tuple(int(round(x * 255)) for x in color)

class Font(object):
    def __init__(self, scene_or_window, unit, name, size, fg=None, bg=None):
        window = scene_or_window
        if isinstance(scene_or_window, Scene):
            window = scene_or_window.window
        self.fg = float_to_byte_color(fg or (1.0, 1.0, 1.0, 1.0))
        self.bg = float_to_byte_color(bg or (0.0, 0.0, 0.0, 0.0))
        if len(self.fg) == 3:
            self.fg += (255,)
        if len(self.bg) == 3:
            self.bg += (255,)
        self.window = window
        self.kerning = {}
        self.load(name, size)
        self.context = Context(TextProgram())
        self.context.sampler = Texture(unit, self.im)
    def render(self, text, coord=(0, 0), anchor=(0, 0)):
        size, positions, uvs = self.generate_vertex_data(text)
        ww, wh = self.window.size
        tx, ty = coord
        ax, ay = anchor
        tw, th = size
        matrix = Matrix()
        matrix = matrix.translate((tx - tw * ax, ty - th * ay, 0))
        matrix = matrix.orthographic(0, ww, wh, 0, -1, 1)
        self.context.matrix = matrix
        vertex_buffer = VertexBuffer(interleave(positions, uvs))
        self.context.position, self.context.uv = vertex_buffer.slices(2, 2)
        glEnable(GL_BLEND)
        glDisable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.context.draw(GL_TRIANGLES)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)
        vertex_buffer.delete()
    def generate_vertex_data(self, text):
        positions = []
        uvs = []
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
            k = self.get_kerning(previous, c) if previous else 0
            x += k
            for i, j in data:
                cx = x + i * self.dx + ox
                cy = y + j * self.dy + oy
                positions.append((cx, cy))
                uvs.append((u + i * self.du, 1 - v - j * self.dv))
            x += ox + sx
            previous = c
        size = (x, self.dy)
        return size, positions, uvs
    def get_kerning(self, c1, c2):
        key = c1 + c2
        if key not in self.kerning:
            a = self.sizes[c1][0] + self.sizes[c2][0]
            b = self.font.getsize(key)[0]
            self.kerning[key] = b - a
        return self.kerning[key]
    def load(self, name, size):
        font = ImageFont.truetype(name, size)
        chars = [chr(x) for x in range(32, 127)]
        sizes = dict((c, font.getsize(c)) for c in chars)
        offsets = dict((c, font.getoffset(c)) for c in chars)
        mw = max(sizes[c][0] for c in chars) + 1
        mh = max(sizes[c][1] for c in chars) + 1
        rows = 10
        cols = 10
        w = mw * cols
        h = mh * rows
        w = int(2 ** ceil(log(w) / log(2)))
        h = int(2 ** ceil(log(h) / log(2)))
        im = Image.new('RGBA', (w, h), self.bg)
        draw = ImageDraw.Draw(im)
        for (row, col), c in zip(product(range(rows), range(cols)), chars):
            x = col * mw
            y = row * mh
            dx, dy = offsets[c]
            draw.text((x + 1 - dx, y + 1 - dy), c, self.fg, font)
        self.dx = mw
        self.dy = mh
        self.du = float(mw) / w
        self.dv = float(mh) / h
        self.sizes = sizes
        self.offsets = offsets
        self.im = im
        self.font = font
