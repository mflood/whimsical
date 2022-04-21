"""
    problem_2021_05.py
"""

import sys
from typing import List, Any, Generator, Iterator 
from dataclasses import dataclass
from enum import IntEnum

from itertools import combinations

import logging
from flood_advent.utils import line_to_parts
from flood_advent.utils import SparseGrid
from flood_advent.utils import init_logging
from flood_advent.utils import LOGGER_NAME
from flood_advent.utils import binary_list_to_int
from flood_advent.utils import parse_args
from flood_advent.utils import Input

logger = logging.getLogger(LOGGER_NAME)

def solve(lines):
    sg = SparseGrid()

    for line in lines:
        logger.debug(line)
        x1, y1, x2, y2 = line.replace('->', ',').replace(' ', '').split(",")
        sg.add_line(int(x1), int(y1), int(x2), int(y2), line, only_horizontal=False)

    # sg.print()
    return(sg.get_num_overlapping_cells())

if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.debug("Logger init")
    year = 2021
    day = 5

    if args.year_day:
        year = int(args.year_day[:4])
        day =int(args.year_day[4:])

    problem_input = Input(year=year, day=day, use_test_data=args.use_test_data)
    lines  = problem_input.get_lines()
    #lines  = problem_input.get_floats()
    #lines  = problem_input.get_ints()

    # convert from generator to list
    lines = list(lines)
    logger.info("Loaded %d values", len(lines))

    if args.print_data:
        for line in lines:
            print(line)

        sys.exit(0)

    ##################### Solution

    print("Solution:", solve(lines=lines))
    print("done.")

# end

