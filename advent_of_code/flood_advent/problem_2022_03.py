"""
    problem_2022_03.py
"""

import sys
import copy
from typing import List, Any, Generator, Iterator
from dataclasses import dataclass
from enum import IntEnum, Enum

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


def item_to_value(item: str) -> int:
    if item.upper() == item:
        return ord(item) - 38

    return ord(item) - 96


def common_letters(line_list: List[str]) -> str:

    bags = copy.copy(line_list)
    sets = []
    for bag in bags:
        as_set = set([*bag])
        sets.append(as_set)

    common_set = sets[0]
    for x in range(1, len(sets)):
        common_set = common_set.intersection(sets[x])
    return list(common_set)
    

def get_value(letter_list: List[str]) -> int:
    total = 0
    for item in letter_list:
        total += item_to_value(item)
    return total


def solve_part_1(lines):

    total = 0
    for line in lines:
        print(line)
        line = line.strip()
        half = int(len(line) / 2)
        start = line[:half]
        end = line[half: ]

        common = common_letters([start, end])
        total += get_value(common)

    return total

def solve_part_2(lines):

    print("solving part 2")
    total = 0
    sets = []
    for line in lines:
        line = line.strip()
        print(line)
        sets.append(line)
        if len(sets) == 3:
            print(f"solving {sets}")
            common = common_letters(sets)
            value = get_value(common)
            print(f"common: {common}: {value}")
            total += value
            sets = []

    return total


def solve(lines, part: int):
    
    if part == 1:
        return solve_part_1(lines=lines)
    else:
        return solve_part_2(lines=lines)

if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.debug("Logger init")
    year = 2022
    day = 3

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
    print("Solution:", solve(lines=lines, part=args.part))
    print("done.")

# end
