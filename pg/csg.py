from __future__ import division
from .core import Mesh
import random

class Vector(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def get_tuple(self):
        return (self.x, self.y, self.z)
    def clone(self):
        return Vector(self.x, self.y, self.z)
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
    def interpolate(self, a, t):
        return self.add(a.subtract(self).multiply(t))

class Vertex(object):
    def __init__(self, position, normal, uv):
        self.position = position
        self.normal = normal
        self.uv = uv
    def clone(self):
        return Vertex(
            self.position.clone(), self.normal.clone(), self.uv.clone())
    def flip(self):
        self.normal = self.normal.negate()
    def interpolate(self, a, t):
        return Vertex(
            self.position.interpolate(a.position, t),
            self.normal.interpolate(a.normal, t),
            self.uv.interpolate(a.uv, t))

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
    def split(self, polygon, co_front, co_back, front, back):
        COPLANAR = 0
        FRONT = 1
        BACK = 2
        BOTH = 3
        EPS = 1e-5
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
                v1 = polygon.vertices[i]
                v2 = polygon.vertices[j]
                t1 = vertex_types[i]
                t2 = vertex_types[j]
                if t1 != BACK:
                    f.append(v1)
                if t1 != FRONT:
                    if t1 != BACK:
                        b.append(v1.clone())
                    else:
                        b.append(v1)
                if (t1 | t2) == BOTH:
                    n = self.w - self.normal.dot(v1.position)
                    d = self.normal.dot(v2.position.subtract(v1.position))
                    v = v1.interpolate(v2, n / d)
                    f.append(v)
                    b.append(v.clone())
            if len(f) >= 3:
                front.append(Polygon(f, polygon.shared))
            if len(b) >= 3:
                back.append(Polygon(b, polygon.shared))

class Polygon(object):
    def __init__(self, vertices, shared):
        self.vertices = vertices
        self.shared = shared
        self.plane = Plane.from_points(*[a.position for a in vertices[:3]])
    def clone(self):
        vertices = [a.clone() for a in self.vertices]
        return Polygon(vertices, self.shared)
    def flip(self):
        self.vertices.reverse()
        for vertex in self.vertices:
            vertex.flip()
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
            return list(polygons)
        front = []
        back = []
        for polygon in polygons:
            self.plane.split(polygon, front, back, front, back)
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
        self.plane = self.plane or random.choice(polygons).plane.clone()
        front = []
        back = []
        for polygon in polygons:
            self.plane.split(polygon, self.polygons, self.polygons, front, back)
        if front:
            self.front = self.front or Node()
            self.front.build(front)
        if back:
            self.back = self.back or Node()
            self.back.build(back)

class Model(object):
    def __init__(self, polygons=None):
        self.polygons = polygons or []
    def clone(self):
        return Model([a.clone() for a in self.polygons])
    def get_polygons(self):
        return self.polygons
    def __or__(self, other):
        return self.union(other)
    def __and__(self, other):
        return self.intersection(other)
    def __sub__(self, other):
        return self.difference(other)
    def __invert__(self):
        return self.inverse()
    def union(self, other):
        a = Node(self.clone().polygons)
        b = Node(other.clone().polygons)
        a.clip_to(b)
        b.clip_to(a)
        b.invert()
        b.clip_to(a)
        b.invert()
        a.build(b.get_polygons())
        return Model(a.get_polygons())
    def difference(self, other):
        a = Node(self.clone().polygons)
        b = Node(other.clone().polygons)
        a.invert()
        a.clip_to(b)
        b.clip_to(a)
        b.invert()
        b.clip_to(a)
        b.invert()
        a.build(b.get_polygons())
        a.invert()
        return Model(a.get_polygons())
    def intersection(self, other):
        a = Node(self.clone().polygons)
        b = Node(other.clone().polygons)
        a.invert()
        b.clip_to(a)
        b.invert()
        a.clip_to(b)
        b.clip_to(a)
        a.build(b.get_polygons())
        a.invert()
        return Model(a.get_polygons())
    def inverse(self):
        polygons = [a.clone() for a in self.polygons]
        for polygon in polygons:
            polygon.flip()
        return Model(polygons)
    def mesh(self):
        positions = []
        normals = []
        uvs = []
        for polygon in self.get_polygons():
            for i in xrange(2, len(polygon.vertices)):
                a = polygon.vertices[0]
                b = polygon.vertices[i - 1]
                c = polygon.vertices[i]
                positions.append(a.position.get_tuple())
                positions.append(b.position.get_tuple())
                positions.append(c.position.get_tuple())
                normals.append(a.normal.get_tuple())
                normals.append(b.normal.get_tuple())
                normals.append(c.normal.get_tuple())
                uvs.append(a.uv.get_tuple()[:2])
                uvs.append(b.uv.get_tuple()[:2])
                uvs.append(c.uv.get_tuple()[:2])
        return Mesh(positions, normals, uvs)

class Solid(Model):
    def __init__(self, shape):
        polygons = []
        for i in xrange(0, len(shape.positions), 3):
            positions = shape.positions[i:i+3]
            normals = shape.normals[i:i+3]
            uvs = shape.uvs[i:i+3]
            vertices = [Vertex(Vector(*a), Vector(*b), Vector(c[0], c[1], 0))
                for a, b, c in zip(positions, normals, uvs)]
            polygon = Polygon(vertices, None)
            polygons.append(polygon)
        super(Solid, self).__init__(polygons)
