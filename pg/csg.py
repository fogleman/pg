from __future__ import division

class Vector(object):
    def __init__(self, *args):
        if len(args) == 0:
            self.x = self.y = self.z = 0
        elif len(args) == 3:
            self.x, self.y, self.z = args
        elif len(args) == 1 and len(args[0]) == 3:
            self.x, self.y, self.z = args[0]
        elif len(args) == 1 and hasattr(args[0], 'x'):
            self.x, self.y, self.z = args[0].x, args[0].y, args[0].z
        else:
            raise Exception
    def clone(self):
        return Vector(self)
    def negate(self):
        return Vector(-self.x, -self.y, -self.z)
    def add(self, a):
        return Vector(self.x + a.x, self.y + a.y, self.z + a.z)
    def subtract(self, a):
        return Vector(self.x - a.x, self.y - a.y, self.z - a.z)
    def multiply(self, a):
        return Vector(self.x * a, self.y * a, self.z * a)
    def divide(self, a):
        return Vector(self.x / a, self.y / a, self.z / a)
    def length(self):
        return self.dot(self) ** 0.5
    def dot(self, a):
        return self.x * a.x + self.y * a.y + self.z * a.z
    def cross(self, a):
        return Vector(
            self.y * a.z - self.z * a.y,
            self.z * a.x - self.x * a.z,
            self.x * a.y - self.y * a.x)
    def normalize(self):
        return self.divide(self.length());
    def lerp(self, a, t):
        return self.add(a.subtract(self).multiply(t))

class Vertex(object):
    def __init__(self, position, normal):
        self.position = Vertex(position)
        self.normal = Vertex(normal)
    def clone(self):
        return Vertex(self.position, self.normal)
    def flip(self):
        self.normal = self.normal.negate()
    def interpolate(self, a, t):
        return Vertex(
            self.position.lerp(a.position, t),
            self.normal.lerp(a.normal, t))

class Plane(object):
    @staticmethod
    def from_points(a, b, c):
        normal = b.subtract(a).cross(c.subtract(a)).normalize()
        return Plane(normal, normal.dot(a))
    def __init__(self, normal, w):
        self.normal = normal
        self.w = w
    def clone(self):
        return Plane(self.normal.clone(), self.w)
    def flip(self):
        self.normal = self.normal.negate()
        self.w = -self.w
    def split(self, polygon):
        COPLANAR = 0
        FRONT = 1
        BACK = 2
        BOTH = 3
        EPS = 1e-5
        front = []
        back = []
        co_front = []
        co_back = []
        polygon_type = 0
        vertex_types = []
        for vertex in polygon.vertices:
            w = self.normal.dot(vertex.position) - self.w
            t = COPLANAR
            if w < -EPS:
                t = BACK
            if w > EPS:
                t = FRONT
            polygon_type |= t
            vertex_types.append(t)
        if polygon_type == COPLANAR:
            if self.normal.dot(polygon.plane.normal) > 0:
                co_front.append(polygon)
            else:
                co_back.append(polygon)
        elif polygon_type == FRONT:
            front.append(polygon)
        elif polygon_type == BACK:
            back.append(polygon)
        else:
            f = []
            b = []
            for i in xrange(len(polygon.vertices)):
                j = (i + 1) % len(polygon.vertices)
                v1, v2 = polygon.vertices[i], polygon.vertices[j]
                t1, t2 = types[i], types[j]
                if t1 != BACK:
                    f.append(v1)
                if t1 != FRONT:
                    if t1 != BACK:
                        b.append(v1.clone())
                    else:
                        b.append(v1)
                if (t1 | t2) == SPANNING:
                    n = self.w - self.normal.dot(v1.position)
                    d = self.normal.dot(v2.position.subtract(v1.position))
                    v = v1.interpolate(v2, n / d)
                    f.append(v)
                    b.append(v.clone())
            if len(f) >= 3:
                front.append(Polygon(f, polygon.shared))
            if len(b) >= 3:
                back.append(Polygon(b, polygon.shared))
        return front, back, co_front, co_back

class Polygon(object):
    def __init__(self, vertices, shared):
        self.vertices = vertices
        self.shared = shared
        self.plane = Plane.from_points(*[a.position for a in vertices[:3]])
    def clone(self):
        vertices = [a.clone() for a in self.vertices]
        return Polygon(vertices, self.shared)
    def flip(self):
        self.vertices = list(reversed(a.flip() for a in self.vertices))
        self.plane.flip()

class Node(object):
    def __init__(self, polygons=None):
        self.plane = None
        self.front = None
        self.back = None
        self.polygons = []
        if polygons:
            self.build(polygons)
    def clone(self):
        node = Node()
        if self.plane:
            node.plane = self.plane.clone()
        if self.front:
            node.front = self.front.clone()
        if self.back:
            node.back = self.back.clone()
        node.polygons = [a.clone() for a in self.polygons]
        return node
    def invert(self):
        for polygon in self.polygons:
            polygon.flip()
        self.plane.flip()
        if self.front:
            self.front.invert()
        if self.back:
            self.back.invert()
        self.front, self.back = self.back, self.front
    def clip_polygons(self, polygons):
        if not self.plane:
            return list(self.polygons)
        front = []
        back = []
        for polygon in self.polygons:
            f, b, cf, cb = self.plane.split(polygon)
            front.extend(f)
            front.extend(cf)
            back.extend(b)
            back.extend(cb)
        if self.front:
            front = self.front.clip_polygons(front)
        if self.back:
            back = self.back.clip_polygons(back)
        else:
            back = []
        return front + back
    def clip_to(self, node):
        self.polygons = node.clip_polygons(self.polygons)
        if self.front:
            self.front.clip_to(node)
        if self.back:
            self.back.clip_to(node)
    def get_polygons(self):
        result = list(self.polygons)
        if self.front:
            result.extend(self.front.get_polygons())
        if self.back:
            result.extend(self.back.get_polygons())
        return result
    def build(self, polygons):
        if not polygons:
            return
        self.plane = self.plane or polygons[0].plane.clone()
        front = []
        back = []
        for polygon in polygons:
            f, b, cf, cb = self.plane.split(polygon)
            front.extend(f)
            front.extend(b)
            self.polygons.extend(cf)
            self.polygons.extend(cb)
        if front:
            self.front = self.front or Node()
            self.front.build(front)
        if back:
            self.back = self.back or Node()
            self.back.build(back)
