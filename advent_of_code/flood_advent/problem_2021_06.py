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


def process(state_list: List[int], num_days: int):

    logger.info("initial state: %s", state_list)

    fish_types = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in state_list:
        fish_types[i] += 1
    logger.info("fish_types day 0: %s", (fish_types))

    for day_idx in range(num_days):
        spawning_fish = fish_types.pop(0)
        fish_types.append(spawning_fish )
        fish_types[6] += spawning_fish
        logger.info("fish_types day %02d: %s", day_idx + 1, fish_types)
    
    return sum(fish_types)
        

def solve(lines):

    data = lines[0]
    data = [int(x) for x in data.split(",")]
    fish_count = process(state_list=data, num_days=256)

    return fish_count

if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.debug("Logger init")
    year = 2021
    day = 6

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

