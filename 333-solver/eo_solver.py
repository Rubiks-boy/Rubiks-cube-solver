from rubiks_cube import rubiks_cube as rc
from copy import deepcopy as copy
from helpers import has_eo, valid_moves, turn_face, face_move_map


def next_valid_moves(prev_moves):
    if len(prev_moves) == 0:
        return valid_moves

    (last_face, _) = prev_moves[-1]
    last_ind = face_move_map[last_face]

    if len(prev_moves) > 1:
        (last2_face, _) = prev_moves[-2]
        last2_ind = face_move_map[last2_face]

        # WLOG, if you spin R then L, you don't want to do either again
        if abs(last2_ind - last_ind) == 3:
            ind = last_ind % 3
            return valid_moves[0:ind*3] + valid_moves[ind*3+3:(ind+3)*3] + valid_moves[(ind+3)*3+3:]

    return valid_moves[0:last_ind*3] + valid_moves[last_ind*3+3:]


def solve_to_EO(scr_cube, max_moves=9001, max_sols=15):
    ''' Solves into: <U,D,L,R,F2,B2> group '''
    cubes_queue = [[]]

    num_moves = 0
    i = 0

    candidates = []

    while(True):
        prev_moves = cubes_queue.pop(0)
        cube = copy(scr_cube)
        for (move, way) in prev_moves:
            cube.turn_face(move, way)

        if num_moves > max_moves:
            # print(f"Reached maximum number of moves: {max_moves}")
            print()
            return candidates

        if len(candidates) > max_sols:
            # print(f"Reached maximum number of EO solutions: {max_sols}")
            print()
            return candidates

        if has_eo(cube):
            candidates.append(prev_moves)

        if num_moves < len(prev_moves):
            num_moves = len(prev_moves)
            # print(f"Now doing {num_moves} moves, {i} iters")
            print('.', end='', flush=True)

        for move in next_valid_moves(prev_moves):
            next_cube = turn_face(cube, move)
            cubes_queue.append(prev_moves + [move])

        i = i+1


if __name__ == '__main__':
    test_cube = rc.Cube()
    test_cube.scramble(
        "B2 L2 D2 R U2 R' F2 U2 F2 L B2 U' F2 L B2 F' D F2 D2 L2")
    # test_cube.scramble(
    #     "B' R' U B2 R2 B L2 U2 F2 D2 F2 U2 L2 U' L' D2 F' L D' B'")

    eo_sols = solve_to_EO(test_cube, max_moves=3)
    print(f"{len(eo_sols)} ways to solve EO in 3 moves")
    eo_sols = solve_to_EO(test_cube, max_moves=4)
    print(f"{len(eo_sols)}+ ways to solve EO in 4 moves")
    print(eo_sols[0])
