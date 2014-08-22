from .core import Mesh
from .util import normal_from_points
from itertools import izip_longest
import os

def parse_obj(path):
    if os.path.exists(path):
        with open(path, 'r') as fp:
            path = fp.read()
    lines = path.split('\n')
    lu_v = []
    lu_vt = []
    lu_vn = []
    positions = []
    normals = []
    uvs = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        args = line.split()
        keyword = args[0]
        args = args[1:]
        if keyword == 'v':
            v = tuple(map(float, args))
            lu_v.append(v)
        elif keyword == 'vt':
            vt = tuple(map(float, args))
            lu_vt.append(vt)
        elif keyword == 'vn':
            vn = tuple(map(float, args))
            lu_vn.append(vn)
        elif keyword == 'f':
            data = [(x + '//').split('/')[:3] for x in args]
            data = [[(int(x) - 1) if x.isdigit() else None for x in row]
                for row in data]
            a = data[0]
            for b, c in zip(data[1:], data[2:]):
                try:
                    n = normal_from_points(*[lu_v[x[0]] for x in [a, b, c]])
                except ZeroDivisionError:
                    continue
                for vertex in [a, b, c]:
                    v, vt, vn = vertex
                    if v is not None:
                        positions.append(lu_v[v])
                    if vt is not None:
                        uvs.append(lu_vt[vt])
                    if vn is not None:
                        normals.append(lu_vn[vn])
                    else:
                        normals.append(n)
    return positions, normals, uvs

def save_obj(self, path):
    lines = []
    v = sorted(set(self.positions))
    vt = sorted(set(self.uvs))
    vn = sorted(set(self.normals))
    lu_v = dict((x, i + 1) for i, x in enumerate(v))
    lu_vt = dict((x, i + 1) for i, x in enumerate(vt))
    lu_vn = dict((x, i + 1) for i, x in enumerate(vn))
    for x in v:
        lines.append('v %f %f %f' % x)
    for x in vt:
        lines.append('vt %f %f' % x)
    for x in vn:
        lines.append('vn %f %f %f' % x)
    f = []
    for v, vt, vn in izip_longest(self.positions, self.uvs, self.normals):
        v = lu_v.get(v, '')
        vt = lu_vt.get(vt, '')
        vn = lu_vn.get(vn, '')
        f.append(('%s/%s/%s' % (v, vt, vn)).strip('/'))
        if len(f) == 3:
            lines.append('f %s' % ' '.join(f))
            f = []
    data = '\n'.join(lines)
    with open(path, 'w') as fp:
        fp.write(data)

Mesh.save_obj = save_obj

class OBJ(Mesh):
    def __init__(self, path):
        super(OBJ, self).__init__()
        positions, normals, uvs = parse_obj(path)
        self.positions = positions
        self.normals = normals
        self.uvs = uvs
