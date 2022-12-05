"""
    problem_2022_01.py
"""

import sys
import copy
from typing import List, Any, Generator, Iterator
from dataclasses import dataclass
from enum import IntEnum

import itertools
import logging
from flood_advent.utils import line_to_parts
from flood_advent.utils import SparseGrid
from flood_advent.utils import init_logging
from flood_advent.utils import LOGGER_NAME
from flood_advent.utils import binary_list_to_int
from flood_advent.utils import parse_args
from flood_advent.utils import Input

logger = logging.getLogger(LOGGER_NAME)

PART_1 = False

class EmptyException(Exception):
    pass

class BreakException(Exception):
    pass


def solve_part_1(lines):
    max_val = 0

    running_total = 0
    for line in lines:
        if not line:
            if running_total > max_val:
                max_val = running_total
            running_total = 0
            continue
        value = int(line)
        running_total += value

    if running_total > max_val:
        max_val = running_total

    return max_val

def solve_part_2(lines):
    totals = []
    running_total = 0
    for line in lines:
        if not line:
            if running_total:
                totals.append(running_total)
            running_total = 0
            continue
        value = int(line)
        running_total += value

    totals.append(running_total)
    totals.sort()
    return sum(totals[-3:])



def solve(lines):
    
    if PART_1:
        return solve_part_1(lines=lines)

    return solve_part_2(lines=lines)
if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.debug("Logger init")
    year = 2022
    day = 1

    if args.year_day:
        year = int(args.year_day[:4])
        day = int(args.year_day[4:])

    problem_input = Input(year=year, day=day, use_test_data=args.use_test_data)
    lines = problem_input.get_lines()
    # lines  = problem_input.get_floats()
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
