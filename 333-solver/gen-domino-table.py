from rubiks_cube import rubiks_cube as rc
from copy import deepcopy as copy
import pickle
from helpers import hash_cube, turn_face, g1_moves, wca_g1_moves

from sys import getsizeof

# How many moves to generate the pruning table up to
max_moves = 8
num_g1_moves = len(g1_moves)


def make_domino_lookup_table():
    g1_sols = dict()
    q = [('', 0)]

    prev_prev_move_len = 0
    iter = 0

    while(len(q) > 0):
        iter = iter+1
        (prev_moves, prev_move_len) = q.pop(0)
        cube = rc.Cube()
        cube.scramble(prev_moves)

        cube_hash = hash_cube(cube)

        if cube_hash not in g1_sols:
            g1_sols[cube_hash] = prev_move_len

            for i in range(num_g1_moves):
                move = g1_moves[i]
                next_cube = turn_face(cube, move)

                if prev_move_len < max_moves:
                    q.append(
                        (f"{prev_moves} {wca_g1_moves[i]}", prev_move_len+1))

        if iter % 10000 == 0:
            print(f"{iter} iterations in")

        if prev_move_len > prev_prev_move_len:
            prev_prev_move_len = prev_move_len
            print(
                f"Now generating table for {prev_move_len} moves, {iter} iters")

    print(f"Finished after performing {iter} iterations")
    return g1_sols


if __name__ == '__main__':
    lookup_table = make_domino_lookup_table()
    with open('domino_lookup.pkl', 'wb') as file:
        pickle.dump(lookup_table, file)
