from .core import Mesh
from .util import normal_from_points
from itertools import izip_longest
import os
import struct

def parse_ascii_stl(data):
    if os.path.exists(data):
        with open(data, 'r') as fp:
            data = fp.read()
    rows = []
    for line in data.split('\n'):
        args = line.strip().lower().split()
        if 'vertex' in args or 'normal' in args:
            rows.append(tuple(map(float, args[-3:])))
    positions = []
    normals = []
    uvs = []
    for i in xrange(0, len(rows), 4):
        n, v1, v2, v3 = rows[i:i+4]
        if not any(n):
            try:
                n = normal_from_points(v1, v2, v3)
            except ZeroDivisionError:
                continue
        positions.extend([v1, v2, v3])
        normals.extend([n, n, n])
    return positions, normals, uvs

def parse_binary_stl(data):
    if os.path.exists(data):
        with open(data, 'rb') as fp:
            data = fp.read()
    positions = []
    normals = []
    uvs = []
    count = struct.unpack('<I', data[80:84])[0]
    for i in xrange(count):
        index = 84 + i * 50
        n, v1, v2, v3 = [struct.unpack('<fff', data[i:i+12]) for i in
            xrange(index, index + 48, 12)]
        if not any(n):
            try:
                n = normal_from_points(v1, v2, v3)
            except ZeroDivisionError:
                continue
        positions.extend([v1, v2, v3])
        normals.extend([n, n, n])
    return positions, normals, uvs

def save_binary_stl(self, path):
    p = self.positions
    data = []
    data.append('\x00' * 80)
    data.append(struct.pack('<I', len(p) / 3))
    for vertices in zip(p[::3], p[1::3], p[2::3]):
        try:
            data.append(struct.pack('<fff', *normal_from_points(*vertices)))
        except ZeroDivisionError:
            data.append(struct.pack('<fff', 0.0, 0.0, 0.0))
        for vertex in vertices:
            data.append(struct.pack('<fff', *vertex))
        data.append(struct.pack('<H', 0))
    data = ''.join(data)
    with open(path, 'wb') as fp:
        fp.write(data)

Mesh.save_binary_stl = save_binary_stl

class STL(Mesh):
    def __init__(self, path):
        super(STL, self).__init__()
        try:
            positions, normals, uvs = parse_binary_stl(path)
        except Exception:
            positions, normals, uvs = parse_ascii_stl(path)
        self.positions = positions
        self.normals = normals
        self.uvs = uvs
