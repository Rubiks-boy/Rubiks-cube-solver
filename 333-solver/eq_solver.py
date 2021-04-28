from rubiks_cube import rubiks_cube as rc
import numpy as np
import pickle
from helpers import hash_cube, turn_face, eo_moves

# when eq_edge_state is dotted with a one-hot binary array,
# result is 0 iff the up and down edges only have
# up and down stickers
eq_cubie = [0, 1, 1, 0, 1, 1]
eq_face = eq_cubie*4 + [0]*6*4
eq_edge_state = eq_face + [0]*6*8*2 + eq_face + [0]*6*8*2


def has_eq_edges(cube):
    bin_arr = cube.get_binary_array(one_hot=True)

    return np.dot(bin_arr, eq_edge_state) == 0


def next_valid_moves(prev_moves):
    if len(prev_moves) == 0:
        return eo_moves

    (last_face, _) = prev_moves[-1]

    return list(filter(lambda m: m[0] != last_face, eo_moves))


def solve_eq_edges(scr_cube, max_moves=9001):
    ''' Given <U,D,L,R,F2,B2> group (EO), solves the front and back crosses '''
    cubes_queue = [(scr_cube, [])]

    num_moves = 0
    i = 0

    candidates = []

    while(True):
        (cube, prev_moves) = cubes_queue.pop(0)

        if num_moves > max_moves:
            # print(f"Reached maximum number of moves: {max_moves}")
            print()
            return candidates

        if num_moves < len(prev_moves):
            num_moves = len(prev_moves)
            # print(f"Now doing {num_moves} moves, {i} iters")
            print('.', end='', flush=True)

        if has_eq_edges(cube):
            candidates.append(prev_moves)
        else:
            for move in next_valid_moves(prev_moves):
                next_cube = turn_face(cube, move)
                cubes_queue.append((next_cube, prev_moves + [move]))

        i = i+1


if __name__ == '__main__':
    test_cube = rc.Cube()
    # Scramble, then solve EO
    test_cube.scramble(
        "B2 L2 D2 R U2 R' F2 U2 F2 L B2 U' F2 L B2 F' D F2 D2 L2")
    test_cube.scramble("U R2 B")

    print(solve_eq_edges(test_cube, max_moves=4))
