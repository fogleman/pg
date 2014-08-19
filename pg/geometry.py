from __future__ import division

from math import asin, pi, atan2, hypot, sin, cos
from .core import Mesh
from .matrix import Matrix
from .util import distance, normalize

class Sphere(Mesh):
    def __init__(self, detail, radius=0.5, center=(0, 0, 0)):
        super(Sphere, self).__init__()
        self.detail = detail
        self.radius = radius
        self.center = center
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
            self.normals.append(a)
            self.normals.append(b)
            self.normals.append(c)
            self.positions.append(tuple(r * a[i] + p[i] for i in xrange(3)))
            self.positions.append(tuple(r * b[i] + p[i] for i in xrange(3)))
            self.positions.append(tuple(r * c[i] + p[i] for i in xrange(3)))
            ta = [0.5 + atan2(a[0], a[2]) / (2 * pi), 0.5 + asin(a[1]) / pi]
            tb = [0.5 + atan2(b[0], b[2]) / (2 * pi), 0.5 + asin(b[1]) / pi]
            tc = [0.5 + atan2(c[0], c[2]) / (2 * pi), 0.5 + asin(c[1]) / pi]
            ab = abs(ta[0] - tb[0])
            ac = abs(ta[0] - tc[0])
            bc = abs(tb[0] - tc[0])
            if any(x > 0.5 for x in [ab, ac, bc]):
                ta[0] = (ta[0] + 1) % 1.0
                tb[0] = (tb[0] + 1) % 1.0
                tc[0] = (tc[0] + 1) % 1.0
            self.uvs.append(tuple(ta))
            self.uvs.append(tuple(tb))
            self.uvs.append(tuple(tc))
        else:
            ab = normalize([(a[i] + b[i]) / 2.0 for i in xrange(3)])
            ac = normalize([(a[i] + c[i]) / 2.0 for i in xrange(3)])
            bc = normalize([(b[i] + c[i]) / 2.0 for i in xrange(3)])
            self._setup(detail - 1, (a, ab, ac))
            self._setup(detail - 1, (b, bc, ab))
            self._setup(detail - 1, (c, ac, bc))
            self._setup(detail - 1, (ab, bc, ac))

class Cone(Mesh):
    def __init__(self, p1, p2, radius, detail):
        super(Cone, self).__init__()
        self.setup(p1, p2, radius, detail)
    def setup(self, p1, p2, radius, detail):
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
        cx, cy, cz = x1 + dx / 2, y1 + dy / 2, z1 + dz / 2
        a = atan2(dz, dx) - pi / 2
        b = atan2(dy, hypot(dx, dz)) - pi / 2
        matrix = Matrix()
        matrix = matrix.rotate((cos(a), 0, sin(a)), b)
        normal_matrix = matrix
        matrix = matrix.translate((cx, cy, cz))
        d = distance(p1, p2)
        y = -sin(pi / 2 - atan2(d, radius)) * radius
        angles = [i * 2 * pi / detail for i in xrange(detail + 1)]
        for a1, a2 in zip(angles, angles[1:]):
            x1, z1 = cos(a1) * radius, sin(a1) * radius
            x2, z2 = cos(a2) * radius, sin(a2) * radius
            y1, y2 = -d / 2, d / 2
            n1, n2 = normalize((x1, y, z1)), normalize((x2, y, z2))
            uv1 = (0.5 + cos(a1) * 0.5, 0.5 + sin(a1) * 0.5)
            uv2 = (0.5 + cos(a2) * 0.5, 0.5 + sin(a2) * 0.5)
            u1 = a1 % (2 * pi)
            u2 = a2 % (2 * pi)
            if u2 < u1:
                u2 += 2 * pi
            positions = [
                (0, y2, 0), (x2, y2, z2), (x1, y2, z1),
                (0, y1, 0), (x1, y2, z1), (x2, y2, z2),
            ]
            normals = [
                (0, 1, 0), (0, 1, 0), (0, 1, 0),
                (0, -1, 0), n1, n2,
            ]
            uvs = [
                (0.5, 0.5), uv1, uv2,
                (0.5, 0.5), uv2, uv1,
            ]
            for position in positions:
                self.positions.append(matrix * position)
            for normal in normals:
                self.normals.append(normal_matrix * normal)
            for uv in uvs:
                self.uvs.append(uv)

class Cylinder(Mesh):
    def __init__(self, p1, p2, radius, detail, hollow=False):
        super(Cylinder, self).__init__()
        self.setup(p1, p2, radius, detail, hollow)
    def setup(self, p1, p2, radius, detail, hollow):
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
        cx, cy, cz = x1 + dx / 2, y1 + dy / 2, z1 + dz / 2
        a = atan2(dz, dx) - pi / 2
        b = atan2(dy, hypot(dx, dz)) - pi / 2
        matrix = Matrix()
        matrix = matrix.rotate((cos(a), 0, sin(a)), b)
        normal_matrix = matrix
        matrix = matrix.translate((cx, cy, cz))
        d = distance(p1, p2)
        angles = [i * 2 * pi / detail for i in xrange(detail + 1)]
        for a1, a2 in zip(angles, angles[1:]):
            x1, z1 = cos(a1) * radius, sin(a1) * radius
            x2, z2 = cos(a2) * radius, sin(a2) * radius
            y1, y2 = -d / 2, d / 2
            n1, n2 = normalize((x1, 0, z1)), normalize((x2, 0, z2))
            uv1 = (0.5 + cos(a1) * 0.5, 0.5 + sin(a1) * 0.5)
            uv2 = (0.5 + cos(a2) * 0.5, 0.5 + sin(a2) * 0.5)
            u1 = a1 % (2 * pi)
            u2 = a2 % (2 * pi)
            if u2 < u1:
                u2 += 2 * pi
            positions = [
                (0, y1, 0), (x1, y1, z1), (x2, y1, z2),
                (0, y2, 0), (x2, y2, z2), (x1, y2, z1),
                (x1, y1, z1), (x1, y2, z1), (x2, y1, z2),
                (x2, y1, z2), (x1, y2, z1), (x2, y2, z2),
            ]
            normals = [
                (0, -1, 0), (0, -1, 0), (0, -1, 0),
                (0, 1, 0), (0, 1, 0), (0, 1, 0),
                n1, n1, n2,
                n2, n1, n2,
            ]
            uvs = [
                (0.5, 0.5), uv1, uv2,
                (0.5, 0.5), uv2, uv1,
                (u1, 0), (u1, 1), (u2, 0),
                (u2, 0), (u1, 1), (u2, 1),
            ]
            if hollow:
                positions = positions[6:]
                normals = normals[6:]
                uvs = uvs[6:]
            for position in positions:
                self.positions.append(matrix * position)
            for normal in normals:
                self.normals.append(normal_matrix * normal)
            for uv in uvs:
                self.uvs.append(uv)

class Cuboid(Mesh):
    def __init__(self, x1, x2, y1, y2, z1, z2):
        super(Cuboid, self).__init__()
        self.setup(x1, x2, y1, y2, z1, z2)
    def setup(self, x1, x2, y1, y2, z1, z2):
        positions = [
            ((x1, y1, z1), (x1, y1, z2), (x1, y2, z1), (x1, y2, z2)),
            ((x2, y1, z1), (x2, y1, z2), (x2, y2, z1), (x2, y2, z2)),
            ((x1, y2, z1), (x1, y2, z2), (x2, y2, z1), (x2, y2, z2)),
            ((x1, y1, z1), (x1, y1, z2), (x2, y1, z1), (x2, y1, z2)),
            ((x1, y1, z1), (x1, y2, z1), (x2, y1, z1), (x2, y2, z1)),
            ((x1, y1, z2), (x1, y2, z2), (x2, y1, z2), (x2, y2, z2)),
        ]
        normals = [
            (-1, 0, 0),
            (1, 0, 0),
            (0, 1, 0),
            (0, -1, 0),
            (0, 0, -1),
            (0, 0, 1),
        ]
        uvs = [
            ((0, 0), (1, 0), (0, 1), (1, 1)),
            ((1, 0), (0, 0), (1, 1), (0, 1)),
            ((0, 1), (0, 0), (1, 1), (1, 0)),
            ((0, 0), (0, 1), (1, 0), (1, 1)),
            ((0, 0), (0, 1), (1, 0), (1, 1)),
            ((1, 0), (1, 1), (0, 0), (0, 1)),
        ]
        indices = [
            (0, 3, 2, 0, 1, 3),
            (0, 3, 1, 0, 2, 3),
            (0, 3, 2, 0, 1, 3),
            (0, 3, 1, 0, 2, 3),
            (0, 3, 2, 0, 1, 3),
            (0, 3, 1, 0, 2, 3),
        ]
        for i in xrange(6):
            for v in xrange(6):
                j = indices[i][v]
                self.positions.append(positions[i][j])
                self.normals.append(normals[i])
                self.uvs.append(uvs[i][j])

class Plane(Mesh):
    def __init__(self, point, normal, size=0.5, both=True):
        super(Plane, self).__init__()
        nx, ny, nz = normal
        self.setup(point, (nx, ny, nz), size)
        if both:
            self.setup(point, (-nx, -ny, -nz), size)
    def setup(self, point, normal, size):
        n = size
        positions = [
            (-n, 0, -n), (n, 0, -n), (-n, 0, n),
            (-n, 0, n), (n, 0, -n), (n, 0, n)
        ]
        uvs = [
            (0, 0), (1, 0), (0, 1),
            (0, 1), (1, 0), (1, 1)
        ]
        normal = normalize(normal)
        nx, ny, nz = normal
        a = atan2(nz, nx) + pi
        b = atan2(ny, hypot(nx, nz)) + pi / 2
        rx, rz = cos(a + pi / 2), sin(a + pi / 2)
        matrix = Matrix()
        matrix = matrix.rotate((0, 1, 0), a)
        matrix = matrix.rotate((rx, 0, rz), b)
        matrix = matrix.translate(point)
        for position in positions:
            self.positions.append(matrix * position)
        self.normals.extend([normal] * 6)
        for uv in uvs:
            self.uvs.append(uv)

class Axes(Mesh):
    def __init__(self, size=1):
        super(Axes, self).__init__()
        n = size
        self.positions = [
            (0, 0, 0), (n, 0, 0),
            (0, 0, 0), (0, n, 0),
            (0, 0, 0), (0, 0, n),
            (0, 0, 0), (-n, 0, 0),
            (0, 0, 0), (0, -n, 0),
            (0, 0, 0), (0, 0, -n),
        ]

class CylinderAxes(Mesh):
    def __init__(self, size=1, radius=0.0625, detail=12):
        super(CylinderAxes, self).__init__()
        n = size
        cylinders = [
            Cylinder((-n, 0, 0), (n, 0, 0), radius, detail),
            Cylinder((0, -n, 0), (0, n, 0), radius, detail),
            Cylinder((0, 0, -n), (0, 0, n), radius, detail),
        ]
        for cylinder in cylinders:
            self.positions.extend(cylinder.positions)
            self.normals.extend(cylinder.normals)
            self.uvs.extend(cylinder.uvs)

class Crosshairs(Mesh):
    def __init__(self, size=10):
        super(Crosshairs, self).__init__()
        n = size
        self.positions = [
            (0, -n), (0, n),
            (-n, 0), (n, 0),
        ]
