from rubiks_cube import rubiks_cube as rc
import numpy as np
from helpers import hash_cube, turn_face, eo_moves, moves_to_wca
from copy import deepcopy as copy
from eo_solver import solve_to_EO
from eq_solver import solve_eq_edges
from co_solver import solve_CO
from domino_solver import solve_from_domino


def solve_cube(cube):
    print("Original cube: ")
    cube.print()

    # Solve for EO
    print("-----SOLVING EO-----")
    eo_sols = solve_to_EO(cube)
    for eo_sol in eo_sols:
        eo_cube = copy(cube)
        wca_eo = moves_to_wca(eo_sol)
        eo_cube.scramble(wca_eo)

        print("Cube with EO:")
        eo_cube.print()

        print("-----SOLVING TOP/BOT CROSS-----")
        eq_sols = solve_eq_edges(eo_cube, max_moves=4)

        # couldn't get edges into the equator within 4 moves
        if len(eq_sols) == 0:
            continue

        for eq_sol in eq_sols:
            eq_cube = copy(eo_cube)
            wca_eq = moves_to_wca(eq_sol)
            eq_cube.scramble(wca_eq)

            print("Cube with EO + top/bot cross:")
            eq_cube.print()

            print("-----SOLVING TO DOMINO-----")
            co_alg = solve_CO(eq_cube)
            eq_cube.scramble(co_alg)

            print("Cube with Domino reduction:")
            eq_cube.print()

            print("-----FINISHING PUZZLE-----")
            domino_sol = solve_from_domino(eq_cube, max_depth=6)
            if domino_sol is not None:
                for (face, way) in domino_sol:
                    eq_cube.turn_face(face, way)
                print("Solved cube!")

                wca_dom = moves_to_wca(domino_sol)
                print("Solution found: ")
                print(f"{wca_eo} {wca_eq} {co_alg} {wca_dom}")


if __name__ == "__main__":
    test_cube = rc.Cube()

    test_cube.scramble(
        "B2 L2 D2 R U2 R' F2 U2 F2 L B2 U' F2 L B2 F' D F2 D2 L2")

    solve_cube(test_cube)
    # first solution it found:
    # R2 U B' R' U R' L' R2 D' R' U2 R' U D R2 U2 R' U' R U L2 U R2 F2 U F2 D' F2 B2 D B2
