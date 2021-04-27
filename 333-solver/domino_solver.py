from rubiks_cube import rubiks_cube as rc
import numpy as np
import pickle
from helpers import g1_moves, hash_cube, turn_face

table_loaded = False
lookup_table = dict()


def load_table():
    global lookup_table
    global table_loaded
    with open('domino_lookup6.pkl', 'rb') as file:
        lookup_table = pickle.load(file)
    table_loaded = True


def recover_sol(cube):
    global lookup_table
    global table_loaded

    if not table_loaded:
        load_table()

    best_candidate = []
    shortest_len = 9001

    if cube.is_solved():
        return []

    hash_val = hash_cube(cube)
    if hash_val not in lookup_table:
        raise Exception("Couldn't recover solution")

    moves_until_solved = lookup_table[hash_val]

    for move in g1_moves:
        cube_to_try = turn_face(cube, move)
        hash_trial = hash_cube(cube_to_try)
        if hash_trial in lookup_table:
            if lookup_table[hash_trial] < moves_until_solved:
                return [move] + recover_sol(cube_to_try)

    raise Exception("Couldn't recover solution")

    return best_candidate


def next_valid_g1_moves(prev_moves):
    if len(prev_moves) == 0:
        return g1_moves

    (last_face, _) = prev_moves[-1]

    return list(filter(lambda m: m[0] != last_face, g1_moves))


def solve_from_domino(scr_cube, max_depth=5):
    ''' Solves the puzzle from a <U,D,L2,R2,F2,B2> group to solved '''
    if not table_loaded:
        load_table()

    cubes_queue = [(scr_cube, [])]

    num_moves = 0
    i = 0

    while(len(cubes_queue) > 0):
        (cube, prev_moves) = cubes_queue.pop(0)
        hash_val = hash_cube(cube)

        if hash_val in lookup_table:
            print(f"Num moves: {len(prev_moves)}\t Iter: {i}")
            return prev_moves + recover_sol(cube)

        if num_moves < len(prev_moves):
            num_moves = len(prev_moves)
            print(f"Now doing {num_moves} moves, {str(i)} iters in")

        if len(prev_moves) < max_depth:
            for move in next_valid_g1_moves(prev_moves):
                next_cube = turn_face(cube, move)
                cubes_queue.append((next_cube, prev_moves + [move]))

        i = i+1

    return None


if __name__ == '__main__':
    test_cube = rc.Cube()
    test_cube.scramble("U2 B2 U2 F2")
    print(recover_sol(test_cube))
    print(solve_from_domino(test_cube))

    test_cube.scramble(
        "D2 F2 D2 R2 B2 U2 F2 R2 L2 U2 F2 U2 B2 F2 L2 U2 B2 D2 B2 F2 U2")
    print(solve_from_domino(test_cube))

    test_cube = rc.Cube()
    # Scramble
    test_cube.scramble(
        "B2 L2 D2 R U2 R' F2 U2 F2 L B2 U' F2 L B2 F' D F2 D2 L2")
    # one EO solution generated
    test_cube.scramble("U R2 B")
    # solve top and bottom crosses
    test_cube.scramble("L F2 D' R")
    # solve CO
    test_cube.scramble("U' R2 D2 R' U' L2 U2 D' R' D L2 U' R")

    test_cube.print()
    print(solve_from_domino(test_cube))
