from itertools import product
from math import ceil, log
from PIL import Image, ImageDraw, ImageFont

class FontTexture(object):
    def __init__(self, name, size):
        self.load(name, size)
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
        im = Image.new('RGBA', (w, h), (0, 0, 0, 255))
        draw = ImageDraw.Draw(im)
        for (row, col), c in zip(product(range(rows), range(cols)), chars):
            x = col * mw
            y = row * mh
            dx, dy = offsets[c]
            # draw.rectangle((x, y, x + mw, y + mh), outline=(48, 48, 48, 255))
            draw.text((x + 1 - dx, y + 1 - dy), c, (255, 255, 255, 255), font)
        self.sizes = sizes
        self.offsets = offsets
        self.kerning = kerning
        self.im = im
