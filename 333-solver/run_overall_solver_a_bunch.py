from scrambles import scrambles
from rubiks_cube import rubiks_cube as rc
from overall_solver import solve_cube
import threading
import concurrent.futures
import timeit
import time
import logging


def run_overall_solver(scramble):
    scr_cube = rc.Cube()
    scr_cube.scramble(scramble)

    start = timeit.timeit()
    (sol, movecount) = solve_cube(scr_cube)
    end = timeit.timeit()

    logging.info((sol, movecount, end-start))


if __name__ == '__main__':
    logging.basicConfig(filename="many_scrambles.log", level=logging.INFO)

    for scramble in scrambles:
        run_overall_solver(scramble)
