from rubiks_cube import rubiks_cube as rc
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


def solve_to_EO(scr_cube, max_moves=9001):
    cubes_queue = [(scr_cube, [])]

    num_moves = 0
    i = 0

    candidates = []

    while(True):
        (cube, prev_moves) = cubes_queue.pop(0)

        if num_moves > max_moves:
            print("Reached maximum number of moves: " + str(max_moves))
            return candidates

        if has_eo(cube):
            candidates.append(prev_moves)

        if num_moves < len(prev_moves):
            num_moves = len(prev_moves)
            print("Now doing " + str(num_moves) +
                  " moves, " + str(i) + " iters")

        for move in next_valid_moves(prev_moves):
            next_cube = turn_face(cube, move)
            cubes_queue.append((next_cube, prev_moves + [move]))

        i = i+1


if __name__ == '__main__':
    test_cube = rc.Cube()
    test_cube.scramble(
        "D B U' R' U R2 L' D F U2 F D2 R2 F2 R2 F2 B' D2 L2 U2 L'")

    print(str(len(solve_to_EO(test_cube, max_moves=3))) +
          " ways to solve EO in 3 moves")
