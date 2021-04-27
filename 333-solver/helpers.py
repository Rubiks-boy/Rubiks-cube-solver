import numpy as np
from copy import deepcopy as copy
from rubiks_cube import rubiks_cube as rc

pows_2 = 2**np.arange(12, dtype=np.uint64)[::-1]
pows_3 = 3**np.arange(8, dtype=np.uint64)[::-1]

g1_moves = [
    ('U', 0),
    ('U', 1),
    ('U', 2),
    ('D', 0),
    ('D', 1),
    ('D', 2),
    ('F', 2),
    ('R', 2),
    ('B', 2),
    ('L', 2),
]


def hash_cube(cube):
    pieces = cube.get_pieces()
    perm = ''.join(pieces[:, 0])
    edge_orient = cube.get_edges_orientation()
    corner_orient = cube.get_corners_orientation()
    return hash(perm) + hash(np.dot(edge_orient, pows_2)) + hash(np.dot(corner_orient, pows_3))


def turn_face(cube, move):
    next_cube = copy(cube)
    (face, way) = move
    next_cube.turn_face(face, way)
    return next_cube


if __name__ == '__main__':
    cube = rc.Cube()
    print(hash_cube(cube))
