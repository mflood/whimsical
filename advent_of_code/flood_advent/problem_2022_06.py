"""
    problem_2022_06.py
"""

import re
import copy
import itertools
import logging
import sys
from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Any, Generator, Iterator, List, Optional

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


def buffer_is_unique(buffer: List[str]):
    return len(set(buffer)) == len(buffer)

def solve_part_1(lines, stream_size: int):

    buffer = [None] * stream_size

    stream = lines[0]

    for idx, x in enumerate(stream):
        buffer.append(x)
        buffer.pop(0)
        print(buffer)
        if None in buffer:
            continue
        if buffer_is_unique(buffer=buffer):
            return idx + 1


def solve_part_2(lines):

    return solve_part_1(lines=lines, stream_size = 14)
    pass


def solve(lines, part: int):

    if part == 1:
        return solve_part_1(lines=lines, stream_size = 4)
    else:
        return solve_part_2(lines=lines)


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.debug("Logger init")
    year = 2022
    day = 6

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
