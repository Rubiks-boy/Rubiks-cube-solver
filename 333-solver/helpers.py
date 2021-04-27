import numpy as np
from copy import deepcopy as copy
from rubiks_cube import rubiks_cube as rc

pows_2 = 2**np.arange(12, dtype=np.uint64)[::-1]
pows_3 = 3**np.arange(8, dtype=np.uint64)[::-1]

face_move_map = {'U': 0, 'F': 1, 'R': 2, 'D': 3, 'B': 4, 'L': 5}

valid_moves = [('U', 0), ('U', 1), ('U', 2),
               ('F', 0), ('F', 1), ('F', 2),
               ('R', 0), ('R', 1), ('R', 2),
               ('D', 0), ('D', 1), ('D', 2),
               ('B', 0), ('B', 1), ('B', 2),
               ('L', 0), ('L', 1), ('L', 2)]

eo_moves = [('U', 0), ('U', 1), ('U', 2),
            ('F', 2),
            ('R', 0), ('R', 1), ('R', 2),
            ('D', 0), ('D', 1), ('D', 2),
            ('B', 2),
            ('L', 0), ('L', 1), ('L', 2)]

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

wca_g1_moves = [
    "U", "U'", "U2",
    "D", "D'", "D2",
    "F2", "R2", "B2", "L2"
]


def has_eo(cube):
    eo = cube.get_edges_orientation()
    return not np.any(eo)


def has_co(cube):
    co = cube.get_corners_orientation()
    return not np.any(co)


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


def moves_to_wca(moves):
    wca_alg = []
    for (move, way) in moves:
        if way == 0:
            curr = move
        elif way == 1:
            curr = f"{move}'"
        else:
            curr = f"{move}2"
        wca_alg.append(curr)
    return " ".join(wca_alg)


def get_wca_movecount(alg):
    str_alg = copy(alg).replace(" ", "").replace("2", "").replace("'", "")
    return len(str_alg)


if __name__ == '__main__':
    cube = rc.Cube()
    print(hash_cube(cube))
