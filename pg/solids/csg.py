from ctypes import *
import os
import pg

dll = CDLL(os.path.join(os.path.dirname(__file__), '_csg.so'))

class List(Structure):
    _fields_ = [
        ('capacity', c_int),
        ('count', c_int),
        ('size', c_int),
        ('data', c_void_p),
    ]

class Vector(Structure):
    _fields_ = [
        ('x', c_float),
        ('y', c_float),
        ('z', c_float),
    ]

class Vertex(Structure):
    _fields_ = [
        ('position', Vector),
        ('normal', Vector),
        ('uv', Vector),
    ]

class Plane(Structure):
    _fields_ = [
        ('normal', Vector),
        ('w', c_float),
    ]

class Polygon(Structure):
    _fields_ = [
        ('plane', Plane),
        ('vertices', Vertex * 3),
    ]

def import_triangles(shape):
    data = pg.interleave(shape.position, shape.normal, shape.uv)
    count = len(data) / 3
    data = pg.flatten(data)
    data = (c_float * len(data))(*data)
    polygons = List()
    dll.list_alloc(byref(polygons), sizeof(Polygon))
    dll.import_triangles(byref(polygons), data, count)
    return polygons

def export_triangles(polygons):
    size = polygons.count * 8 * 3
    data = (c_float * size)()
    dll.export_triangles(byref(polygons), data)
    return list(data)

class Solid(object):
    def __init__(self, polygons=None):
        if not isinstance(polygons, List):
            polygons = import_triangles(polygons)
        self.polygons = polygons
    def __del__(self):
        dll.list_free(byref(self.polygons))
    def get_data(self):
        data = export_triangles(self.polygons)
        return [tuple(data[i:i+8]) for i in xrange(0, len(data), 8)]
    def __or__(self, other):
        return self.union(other)
    def __and__(self, other):
        return self.intersection(other)
    def __sub__(self, other):
        return self.difference(other)
    def __invert__(self):
        return self.inverse()
    def union(self, other):
        polygons = List()
        dll.list_alloc(byref(polygons), sizeof(Polygon))
        dll.csg_union(byref(polygons), byref(self.polygons), byref(other.polygons))
        return Solid(polygons)
    def intersection(self, other):
        polygons = List()
        dll.list_alloc(byref(polygons), sizeof(Polygon))
        dll.csg_intersection(byref(polygons), byref(self.polygons), byref(other.polygons))
        return Solid(polygons)
    def difference(self, other):
        polygons = List()
        dll.list_alloc(byref(polygons), sizeof(Polygon))
        dll.csg_difference(byref(polygons), byref(self.polygons), byref(other.polygons))
        return Solid(polygons)
    def inverse(self):
        polygons = List()
        dll.list_alloc(byref(polygons), sizeof(Polygon))
        dll.csg_inverse(byref(polygons), byref(self.polygons))
        return Solid(polygons)
