from rubiks_cube import rubiks_cube as rc
import numpy as np
from helpers import hash_cube, turn_face, eo_moves, moves_to_wca, get_wca_movecount
from copy import deepcopy as copy
from eo_solver import solve_to_EO
from eq_solver import solve_eq_edges
from co_solver import solve_CO
from domino_solver import solve_from_domino

max_domino_moves = 14


def solve_cube(cube):
    best_sol = ""
    best_sol_len = 9001

    print("Original cube: ")
    cube.print()

    # Solve for EO
    print("Solving EO.", end='', flush=True)
    eo_sols = solve_to_EO(cube)
    for eo_sol in eo_sols:
        eo_cube = copy(cube)
        wca_eo = moves_to_wca(eo_sol)
        eo_cube.scramble(wca_eo)

        # print("Cube with EO:")
        # eo_cube.print()

        print("Solving top/bot cross.", end='', flush=True)
        eq_sols = solve_eq_edges(eo_cube, max_moves=4)

        # couldn't get edges into the equator within 4 moves
        if len(eq_sols) == 0:
            continue

        for eq_sol in eq_sols:
            eq_cube = copy(eo_cube)
            wca_eq = moves_to_wca(eq_sol)
            eq_cube.scramble(wca_eq)

            # print("Cube with EO + top/bot cross:")
            # eq_cube.print()

            print("Solving to Domino.", flush=True)
            co_alg = solve_CO(eq_cube)
            eq_cube.scramble(co_alg)

            # print("Cube with Domino reduction:")
            # eq_cube.print()

            # Calculate movecount from EO + Cross + CO
            if co_alg is None:
                continue

            co_movecount = get_wca_movecount(co_alg)
            movecount_so_far = co_movecount + len(eq_sol) + len(eo_sol)

            remaining_movecount = min(
                best_sol_len - movecount_so_far - 1, max_domino_moves)

            print(
                f"Finishing puzzle ({remaining_movecount}).", end='', flush=True)
            domino_sol = solve_from_domino(
                eq_cube, max_depth=remaining_movecount)
            if domino_sol is not None:
                wca_dom = moves_to_wca(domino_sol)
                eq_cube.scramble(wca_dom)

                sol = f"{wca_eo} {wca_eq} {co_alg} {wca_dom}"
                movecount = movecount_so_far + len(domino_sol)

                if movecount < best_sol_len:
                    best_sol_len = movecount
                    best_sol = sol

                print("~~~~~~~~Solved cube!~~~~~~~~")
                print(f"Solution ({movecount}): {sol}")

    return (best_sol, best_sol_len)


if __name__ == "__main__":
    test_cube = rc.Cube()

    test_cube.scramble(
        "B2 L2 D2 R U2 R' F2 U2 F2 L B2 U' F2 L B2 F' D F2 D2 L2")
    # test_cube.scramble(
    #     "D B2 L' R2 D2 B2 L2 U' R2 F2 D' F2 D2 U B' L F D' U' B2 U'")

    (sol, movecount) = solve_cube(test_cube)
    test_cube.scramble(sol)

    if(test_cube.is_solved()):
        print(f"Solution worked!: {sol}")
    else:
        print(f"Solution didn't work :/ : {sol}")
