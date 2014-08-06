from operator import add

def hex_color(value):
    r = ((value >> (8 * 2)) & 255) / 255.0
    g = ((value >> (8 * 1)) & 255) / 255.0
    b = ((value >> (8 * 0)) & 255) / 255.0
    return (r, g, b)

def normalize(vector):
    d = sum(x * x for x in vector) ** 0.5
    return tuple(x / d for x in vector)

def distance(p1, p2):
    return sum((a - b) ** 2 for a, b in zip(p1, p2)) ** 0.5

def interleave(*args):
    return [reduce(add, x) for x in zip(*args)]

def flatten(x):
    return reduce(add, x)
