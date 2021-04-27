from copy import deepcopy as copy
from rubiks_cube import rubiks_cube as rc
import numpy as np
from helpers import has_co, wca_g1_moves, get_wca_movecount

# Every possible Corner orientation can be solved using one of these algs
# Pulled from EPOCLL section of: https://www.speedsolving.com/threads/lcbm-long-comeau-belt-method-guide-and-algorithms.30102/
co_algs = [
    "",
    "R' U' R' U R U2 D R' D' R",
    "R' U' R U2 R U' D R2 U R'",
    "U' R U' D L2 R2 D' L2 U R'",
    "R' U2 R' U D R2 U2 R' U' R",
    "L D' L' U' L2 D2 L' D' L'",
    "R D L2 R' D R D2 L2 R'",
    "L U D L' U D2 L' U2 D L'",
    "L U L' U2 L' U D' L2 U' L",
    "L' U L U' L U' D2 L U L'",
    "U' L' U D' R2 L2 D R2 U' L",
    "U R U' R2 D2 R U2 R U' R'",
    "R' U2 D2 R' D R2 U2 D R",
    "L U R U' L U2 L2 U' R'",
    "R U2 L2 U R U D L2 R D R",
    "D R U D' L2 R2 U' L2 D R'",
    "D' L' U' D L2 R2 U R2 D' L",
    "R2 U' D L U D' L2 R2 D U' L",
    "R D R' U D2 R2 D2 R' D' R'",
    "L D L' U' D2 L2 D2 L' D' L'",
    "L U' L2 R2 U' L' R2 U D2 L",
    "R' U' L2 U R2 U' D L2 R' D' U R'",
    "R U' R2 D L' R2 U R' U' L",
    "L' U R U' L R2 D R2 U R'",
    "R U R' U2 D R2 U2 R' U' R'",
    "U2 L' U L' U' L2 D' L D L'",
    "R U' D R U' R' U2 D' R'",
    "D' L' U' L' U2 L U' L",
    "L' U R U2 R' U L R U R'",
    "L U' L' D' L2 U2 L' U' L'",
    "R' U2 D2 R' U R2 U D2 R",
    "L U L' U2 D' L2 U2 L' U' L'",
    "L2 U2 L' U' L U2 L' U' L'",
    "R U2 D2 R' U2 D2 R'",
    "U R U D2 R' U' D2 R'",
    "L' U' L R2 D' R2 U' L' U2 L",
    "R U L2 U2 L' U R' U' L'",
    "L D R D' L D2 L2 D' R'",
    "L U L2 U' L U' D2 L U2 L",
    "U' L' D' L' D2 L D' L",
    "D R U2 D R' U2 D' R'",
    "L U' D' L U D L'",
    "L' U' L2 U' L' U2 D' L2 U' L'",
    "L U D L' U2 D L' U D2 L'",
    "D R U L2 U D R U2 L2 D' R'",
    "R' U L2 U' R2 U D' L2 R U' D R'",
    "R' U' L2 U2 D' R' D L2 U' R",
    "L' U' L2 D2 L U2 D' L U' L",
    "D L' U' D' L D R2 U L R2",
    "L U D L' U2 D2 L U D L'"
]

pows_3 = 3**np.arange(8, dtype=np.uint64)[::-1]

alg_lookup = dict()

parity_moves = []
g1_plus_null = [""] + wca_g1_moves
for m1 in g1_plus_null:
    for m2 in g1_plus_null:
        if m1 == m2 and m1 != "":
            continue
        for m3 in ["F2", "R2", "B2", "L2"]:
            if m2 == m3:
                continue
            parity_moves.append(' '.join(filter(None, [m1, m2, m3])))


orient_moves_for_alg = ["", "U", "U'", "U2",
                        "D", "D'", "D2",
                        "U D", "U' D", "U2 D",
                        "U D'", "U' D'", "U2 D'",
                        "U D2", "U' D2", "U2 D2"]


def test_co_algs(prealg_cube):
    for alg in co_algs:
        candidate = copy(prealg_cube)
        candidate.scramble(alg)
        if has_co(candidate):
            return alg
    return None


def solve_CO(cube):
    ''' Takes a cube with EO + edges in equator to <U,D,L2,R2,F2,B2> group '''

    best_len = 9001
    best_candidate = []

    for parity in parity_moves:
        parity_cube = copy(cube)
        parity_cube.scramble(parity)

        for pre_orient in orient_moves_for_alg:
            prealg_cube = copy(parity_cube)
            prealg_cube.scramble(pre_orient)

            co_hash = hash(
                np.dot(prealg_cube.get_corners_orientation(), pows_3))

            if co_hash in alg_lookup:
                alg = alg_lookup[co_hash]
            else:
                alg = test_co_algs(prealg_cube)
                alg_lookup[co_hash] = alg

            if alg is not None:
                movecount = get_wca_movecount(f"{parity} {pre_orient} {alg}")

                if movecount < best_len:
                    best_len = movecount
                    best_candidate = f"{parity} {pre_orient} {alg}"

        if best_len < 9001:
            return best_candidate


if __name__ == '__main__':
    test_cube = rc.Cube()
    # Scramble
    test_cube.scramble(
        "B2 L2 D2 R U2 R' F2 U2 F2 L B2 U' F2 L B2 F' D F2 D2 L2")
    # one EO solution generated
    test_cube.scramble("U R2 B")
    # solve top and bottom crosses
    test_cube.scramble("L F2 D' R")

    print(solve_CO(test_cube))
