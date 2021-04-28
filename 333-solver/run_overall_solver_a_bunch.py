from scrambles import scrambles
from rubiks_cube import rubiks_cube as rc
from overall_solver import solve_cube
import time
import logging


def run_overall_solver(scramble):
    scr_cube = rc.Cube()
    scr_cube.scramble(scramble)

    start = time.time()
    (sol, movecount) = solve_cube(scr_cube)
    end = time.time()

    logging.info((scramble, sol, movecount, end-start))


if __name__ == '__main__':
    logging.basicConfig(filename="many_scrambles_eo-2.log", level=logging.INFO)

    for scramble in scrambles:
        run_overall_solver(scramble)
