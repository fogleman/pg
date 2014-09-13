from math import ceil, log

class Node(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.right = None
        self.down = None
    def insert(self, w, h):
        if self.right:
            result = self.right.insert(w, h)
            if result:
                return result
            result = self.down.insert(w, h)
            if result:
                return result
            return None
        elif w <= self.w and h <= self.h:
            self.right = Node(self.x + w, self.y, self.w - w, h)
            self.down = Node(self.x, self.y + h, self.w, self.h - h)
            return (self.x, self.y, w, h)
        else:
            return None

def pot(x):
    return 2 ** int(ceil(log(x) / log(2)))

def estimate_size(sizes):
    a = sum(w * h for w, h in sizes)
    mw = max(w for w, h in sizes)
    mh = max(h for w, h in sizes)
    w1 = pot(mw)
    h1 = pot(mh)
    w2 = pot(a ** 0.5)
    h2 = pot(float(a) / w2)
    return (max(w1, w2), max(h1, h2))

def try_pack(tw, th, items):
    result = []
    node = Node(0, 0, tw, th)
    for index, (w, h) in items:
        position = node.insert(w, h)
        if position is None:
            return None
        result.append((index, position))
    result.sort()
    result = [x[1] for x in result]
    return result

def pack(sizes):
    items = enumerate(sizes)
    items = sorted(items, key=lambda x: max(x[1]), reverse=True)
    tw, th = estimate_size(sizes)
    while True:
        result = try_pack(tw, th, items)
        if result:
            return (tw, th), result
        if tw <= th:
            tw *= 2
        else:
            th *= 2
