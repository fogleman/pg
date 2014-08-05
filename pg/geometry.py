from math import asin, pi, atan2
from util import normalize

class Sphere(object):
    def __init__(self, detail, radius=0.5, center=(0, 0, 0)):
        self.detail = detail
        self.radius = radius
        self.center = center
        self.position = []
        self.uv = []
        self.setup()
    def setup(self):
        indices = [
            (0, 3, 4), (0, 4, 1), (5, 4, 3), (5, 1, 4),
            (2, 3, 0), (1, 2, 0), (3, 2, 5), (2, 1, 5),
        ]
        positions = [
            (0, 0, -1), (1, 0, 0), (0, -1, 0),
            (-1, 0, 0), (0, 1, 0), (0, 0, 1),
        ]
        for a, b, c in indices:
            position = (positions[a], positions[b], positions[c])
            self._setup(self.detail, position)
    def _setup(self, detail, position):
        a, b, c = position
        r = self.radius
        p = self.center
        if detail == 0:
            self.position.extend([r * a[i] + p[i] for i in xrange(3)])
            self.position.extend([r * b[i] + p[i] for i in xrange(3)])
            self.position.extend([r * c[i] + p[i] for i in xrange(3)])
            ta = [0.5 + atan2(a[0], a[2]) / (2 * pi), 0.5 - asin(a[1]) / pi]
            tb = [0.5 + atan2(b[0], b[2]) / (2 * pi), 0.5 - asin(b[1]) / pi]
            tc = [0.5 + atan2(c[0], c[2]) / (2 * pi), 0.5 - asin(c[1]) / pi]
            ab = abs(ta[0] - tb[0])
            ac = abs(ta[0] - tc[0])
            bc = abs(tb[0] - tc[0])
            if any(x > 0.5 for x in [ab, ac, bc]):
                ta[0] = (ta[0] + 1) % 1.0
                tb[0] = (tb[0] + 1) % 1.0
                tc[0] = (tc[0] + 1) % 1.0
            self.uv.extend(ta)
            self.uv.extend(tb)
            self.uv.extend(tc)
        else:
            ab = normalize([(a[i] + b[i]) / 2.0 for i in xrange(3)])
            ac = normalize([(a[i] + c[i]) / 2.0 for i in xrange(3)])
            bc = normalize([(b[i] + c[i]) / 2.0 for i in xrange(3)])
            self._setup(detail - 1, (a, ab, ac))
            self._setup(detail - 1, (b, bc, ab))
            self._setup(detail - 1, (c, ac, bc))
            self._setup(detail - 1, (ab, bc, ac))
