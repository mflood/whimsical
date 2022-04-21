"""
    problem_2021_06.py
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

PART_1 = False

def get_cost(target_position, i):
    if PART_1:
        # part 1 cost
        return abs(i - target_position)

    # Part 2
    distance = abs(i - target_position)

    if distance % 2:
        pair_cost = distance // 2
        adjustment = pair_cost + 1
        cost = (distance + 1) * pair_cost + adjustment
        # logger.info("Cost from %d to %d (distance %s) is %s", i, target_position, distance, cost)
        return cost
    else:
        pair_cost = distance // 2
        adjustment = pair_cost 
        cost = (distance) * pair_cost + adjustment
        #logger.info("Cost from %d to %d (distance %s) is %s (pair %s adjustment %s)", i, target_position, distance, cost, pair_cost, adjustment)
        return cost



def process(state_list: List[int]):

    logger.info("initial state: %s", state_list)

    max_x = max(state_list)

    lowest_cost = None
    for target_position in range(max_x):
        #logger.info("Eval moving to position %d", target_position)
        cost = 0
        for i in state_list:
            cost += get_cost(target_position=target_position, i=i)

            #logger.info("Move from %d to %d: %d fuel", i, target_position, cost)
        if lowest_cost is None or cost < lowest_cost:
            lowest_cost = cost
        #logger.info("")
    return lowest_cost 
        

def solve(lines):

    data = lines[0]
    data = [int(x) for x in data.split(",")]
    fuel = process(state_list=data)

    return fuel

if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.debug("Logger init")
    year = 2021
    day = 7

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

