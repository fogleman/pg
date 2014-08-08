from math import floor
import random

F2 = (3 ** 0.5 - 1) * 0.5
G2 = (3 - 3 ** 0.5) / 6.0

GRAD = [
    (1, 1, 0), (-1, 1, 0), (1, -1, 0), (-1, -1, 0),
    (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
    (0, 1, 1), (0, -1, 1), (0, 1, -1), (0, -1, -1),
    (1, 1, 0), (0, -1, 1), (-1, 1, 0), (0, -1, -1),
]

PERM = [
    151, 160, 137,  91,  90,  15, 131,  13,
    201,  95,  96,  53, 194, 233,   7, 225,
    140,  36, 103,  30,  69, 142,   8,  99,
     37, 240,  21,  10,  23, 190,   6, 148,
    247, 120, 234,  75,   0,  26, 197,  62,
     94, 252, 219, 203, 117,  35,  11,  32,
     57, 177,  33,  88, 237, 149,  56,  87,
    174,  20, 125, 136, 171, 168,  68, 175,
     74, 165,  71, 134, 139,  48,  27, 166,
     77, 146, 158, 231,  83, 111, 229, 122,
     60, 211, 133, 230, 220, 105,  92,  41,
     55,  46, 245,  40, 244, 102, 143,  54,
     65,  25,  63, 161,   1, 216,  80,  73,
    209,  76, 132, 187, 208,  89,  18, 169,
    200, 196, 135, 130, 116, 188, 159,  86,
    164, 100, 109, 198, 173, 186,   3,  64,
     52, 217, 226, 250, 124, 123,   5, 202,
     38, 147, 118, 126, 255,  82,  85, 212,
    207, 206,  59, 227,  47,  16,  58,  17,
    182, 189,  28,  42, 223, 183, 170, 213,
    119, 248, 152,   2,  44, 154, 163,  70,
    221, 153, 101, 155, 167,  43, 172,   9,
    129,  22,  39, 253,  19,  98, 108, 110,
     79, 113, 224, 232, 178, 185, 112, 104,
    218, 246,  97, 228, 251,  34, 242, 193,
    238, 210, 144,  12, 191, 179, 162, 241,
     81,  51, 145, 235, 249,  14, 239, 107,
     49, 192, 214,  31, 181, 199, 106, 157,
    184,  84, 204, 176, 115, 121,  50,  45,
    127,   4, 150, 254, 138, 236, 205,  93,
    222, 114,  67,  29,  24,  72, 243, 141,
    128, 195,  78,  66, 215,  61, 156, 180,
]

class Noise(object):
    def __init__(self, seed=None):
        self.seed(seed)
    def seed(self, seed=None):
        perm = list(PERM)
        if seed is not None:
            random.Random(seed).shuffle(perm)
        self.perm = perm + perm
    def _simplex2(self, x, y):
        perm = self.perm
        s = (x + y) * F2
        i = floor(x + s)
        j = floor(y + s)
        t = (i + j) * G2
        x0 = x - (i - t)
        y0 = y - (j - t)
        i1 = int(x0 > y0)
        j1 = int(x0 <= y0)
        x1 = x0 - i1 + G2
        y1 = y0 - j1 + G2
        x2 = x0 + G2 * 2 - 1
        y2 = y0 + G2 * 2 - 1
        i = int(i) % 256
        j = int(j) % 256
        noise = 0.0
        f = 0.5 - x0 * x0 - y0 * y0
        if f > 0:
            gx, gy, _ = GRAD[perm[i + perm[j]] % 12]
            noise += f * f * f * f * (gx * x0 + gy * y0)
        f = 0.5 - x1 * x1 - y1 * y1
        if f > 0:
            gx, gy, _ = GRAD[perm[i + i1 + perm[j + j1]] % 12]
            noise += f * f * f * f * (gx * x1 + gy * y1)
        f = 0.5 - x2 * x2 - y2 * y2
        if f > 0:
            gx, gy, _ = GRAD[perm[i + 1 + perm[j + 1]] % 12]
            noise += f * f * f * f * (gx * x2 + gy * y2)
        return noise * 70
    def simplex2(self, x, y, octaves=1, persistence=0.5, lacunarity=2.0):
        frequency = 1.0
        amplitude = 1.0
        maximum = 1.0
        total = self._simplex2(x, y)
        for _ in xrange(octaves - 1):
            frequency *= lacunarity
            amplitude *= persistence
            maximum += amplitude
            total += self._simplex2(x * frequency, y * frequency) * amplitude
        return total / maximum

_instance = Noise()

def simplex2(x, y, octaves=1, persistence=0.5, lacunarity=2.0):
    return _instance.simplex2(x, y, octaves, persistence, lacunarity)
