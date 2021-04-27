from rubiks_cube import rubiks_cube as rc
from copy import deepcopy as copy
import pickle
from helpers import hash_cube, turn_face, g1_moves

# How many moves to generate the pruning table up to
max_moves = 8


def make_domino_lookup_table():
    g1_sols = dict()
    q = [(copy(rc.Cube()), [])]

    prev_prev_move_len = 0
    i = 0

    while(len(q) > 0):
        i = i+1
        (cube, prev_moves) = q.pop(0)

        cube_hash = hash_cube(cube)

        if cube_hash not in g1_sols:
            g1_sols[cube_hash] = len(prev_moves)

            for move in g1_moves:
                next_cube = turn_face(cube, move)
                q.append((next_cube, prev_moves + [move]))

        prev_move_len = len(prev_moves)

        if i % 10000 == 0:
            print(str(i) + " iterations in")
        if prev_move_len > max_moves:
            print("Finished after performing " + str(i) + " iterations")
            return g1_sols

        if prev_move_len > prev_prev_move_len:
            prev_prev_move_len = prev_move_len
            print("Now generating table for " +
                  str(prev_move_len) + " moves, " + str(i))

    return g1_sols


if __name__ == '__main__':
    lookup_table = make_domino_lookup_table()
    with open('domino_lookup.pkl', 'wb') as file:
        pickle.dump(lookup_table, file)
