"""
    problem_2022_05.py
"""

import copy
import itertools
import logging
import sys
from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Any, Generator, Iterator, List

from flood_advent.utils import (
    LOGGER_NAME,
    Input,
    SparseGrid,
    binary_list_to_int,
    init_logging,
    line_to_parts,
    parse_args,
)

logger = logging.getLogger(LOGGER_NAME)


@dataclass
class Range:
    my_range_string: str

    @property
    def min(self) -> int:
        return int(self.my_range_string.split("-")[0])

    @property
    def max(self) -> int:
        return int(self.my_range_string.split("-")[1])

    def contains(self, number: int) -> bool:
        return self.min <= number and self.max >= number

    def contains_range(self, other_range) -> bool:
        return self.min <= other_range.min and self.max >= other_range.max

    def overlaps_range(self, other_range) -> bool:
        return self.max >= other_range.min and self.min <= other_range.max


def print_range_pair(r1: Range, r2: Range):

    for r in [r1, r2]:
        buffer = []
        for x in range(max(r1.max + 1, r2.max + 1, 10)):
            if r.contains(x):
                buffer.append(str(x))
            else:
                buffer.append(".")

        buffer.append(" ")
        buffer.append(r.my_range_string)
        print("".join(buffer))
    print("")


def get_ranges(line: str) -> List[Range]:
    r1, r2 = line.split(",")
    range1 = Range(r1)
    range2 = Range(r2)
    return [range1, range2]


def solve_part_1(lines):

    total = 0
    for line in lines:
        r1, r2 = get_ranges(line)
        print_range_pair(r1, r2)
        if r1.contains_range(r2) or r2.contains_range(r1):
            total += 1

    return total


def solve_part_2(lines):

    print("solving part 2")
    total = 0
    for line in lines:
        r1, r2 = get_ranges(line)
        print_range_pair(r1, r2)
        if r1.overlaps_range(r2):
            total += 1

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
    day = 5

    if args.year_day:
        year = int(args.year_day[:4])
        day = int(args.year_day[4:])

    problem_input = Input(year=year, day=day, use_test_data=args.use_test_data)
    line_iter = problem_input.get_lines()
    # lines  = problem_input.get_floats()
    # lines  = problem_input.get_ints()

    # convert from generator to list
    lines = list(line_iter)
    logger.info("Loaded %d values", len(lines))

    if args.print_data:
        for line in lines:
            print(line)

        sys.exit(0)

    # Solution
    print("Solution:", solve(lines=lines, part=args.part))
    print("done.")

# end
