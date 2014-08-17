from .util import normal_from_points
import os

def parse_obj(path):
    if os.path.exists(path):
        with open(path, 'r') as fp:
            path = fp.read()
    lines = path.split('\n')
    lu_v = []
    lu_vt = []
    lu_vn = []
    position = []
    normal = []
    uv = []
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
                        position.append(lu_v[v])
                    if vt is not None:
                        uv.append(lu_vt[vt])
                    if vn is not None:
                        normal.append(lu_vn[vn])
                    else:
                        normal.append(n)
    return position, normal, uv

class OBJ(object):
    def __init__(self, path):
        position, normal, uv = parse_obj(path)
        self.position = position
        self.normal = normal
        self.uv = uv
