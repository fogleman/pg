from itertools import product
from math import ceil, log
from PIL import Image, ImageDraw, ImageFont

def render_char(w, h, font, c):
    im = Image.new('RGBA', (w * 2, h * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    draw.text((w / 2, h / 2), c, (255, 255, 255, 255), font)
    box = im.getbbox()
    return box, im.crop(box)

def render_font(name, size):
    font = ImageFont.truetype(name, size)
    rows = cols = 10
    chars = [chr(x) for x in range(32, 127)]
    # widths = dict((c, font.getsize(c)[0]) for c in chars)
    # for c1, c2 in product(chars, repeat=2):
    #     a = widths[c1] + widths[c2]
    #     b = font.getsize(c1 + c2)[0]
    #     k = b - a
    cw = max(font.getsize(c)[0] for c in chars) + 2
    ch = max(font.getsize(c)[1] for c in chars) + 2
    w = cw * cols
    h = ch * rows
    w = int(2 ** ceil(log(w) / log(2)))
    h = int(2 ** ceil(log(h) / log(2)))
    im = Image.new('RGBA', (w, h), (0, 0, 0, 255))
    draw = ImageDraw.Draw(im)
    for (row, col), text in zip(product(range(rows), range(cols)), chars):
        tw, th = font.getsize(text)
        x = col * cw
        y = row * ch
        # draw.rectangle((c * cw, r * ch, c * cw + cw, r * ch + ch),
        #     outline=(32, 0, 0, 255))
        draw.rectangle((x, y, x + cw, y + ch),
            outline=(128, 0, 0, 255))
        box, cim = render_char(cw, ch, font, text)
        l, t, r, b = box or (0, 0, cw, ch)
        tw, th = (r - l, b - t)
        dx, dy = (cw / 2 - tw / 2, ch / 2 - th / 2)
        # im.paste(cim, (x + 1 + (cw - r + l) / 2, y + 1 + (ch - b + t) / 2), cim)
        im.paste(cim, (x + 1 + dx, y + 1 + dy), cim)
    im.save('output.png')

class FontTexture(object):
    pass

if __name__ == '__main__':
    render_font('Arial.ttf', 48)
    # render_font('Chalkduster.ttf', 48)
    # main()
