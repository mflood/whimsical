"""
    problem_2021_09.py
"""

import sys
from typing import List, Any, Generator, Iterator 
from dataclasses import dataclass
import pprint
from enum import IntEnum

import copy
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

def is_low_point(lines, w, h, x, y):
    logger.debug("is_low_point(%d, %d, %d, %d)", w, h, x, y)
    val = lines[y][x]
    for neighbor in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = neighbor
        nx += x
        ny += y
        #logger.debug("Looking at neighbor: %d, %d", nx, ny)
        if ny < 0 or ny >= h or nx < 0 or nx >= w:
            logger.debug("%s, %s is out of bounds", nx, ny)
            continue
        nval = lines[ny][nx]
        if int(nval) <= int(val):
            #logger.debug("neighbor %s is greater than point %s, not a low point", nval, val)
            return False
    logger.info("found low point: %s, %s", x, y)
    return True


def get_low_points(lines):

    w = len(lines[0])
    h = len(lines)
    return_list = []
    for y in range(h):
        for x in range(w):
            if is_low_point(lines, w, h, x, y):
                return_list.append(int(lines[y][x]))

    return return_list

def get_low_points_coord(lines):

    w = len(lines[0])
    h = len(lines)
    return_list = []
    for y in range(h):
        for x in range(w):
            if is_low_point(lines, w, h, x, y):
                return_list.append((x, y))

    return return_list

def get_higher_neighbors(lines, w, h, x, y):

    return_set = []
    val = int(lines[y][x])
    logger.debug("Getting higher neighbors for %s, %s (val %s)", x, y, val)
    for neighbor in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = neighbor
        nx += x
        ny += y
        if ny < 0 or ny >= h or nx < 0 or nx >= w:
            continue
        nval = lines[ny][nx]
        if int(nval) > val and int(nval) < 9:

            logger.debug("%s %s is a higher neighbor (val %s)", nx, ny, nval)
            return_set.append((nx, ny))
            return_set.extend(get_higher_neighbors(lines, w, h, nx, ny))
        else:
            logger.debug("%s %s is not a higher neighbor (val %s)", nx, ny, nval)

    return return_set

def get_basin_sizes(lines):

    w = len(lines[0])
    h = len(lines)

    low_points = get_low_points_coord(lines)
    logger.debug("Low points: %s", low_points)
    sizes = []
    for point in low_points:
        x, y = point
        n_set = get_higher_neighbors(lines, w, h, x, y)
        n_set.append(point)
        reduced = list(set(n_set))
        logger.debug("basin %s, %s: %s", x, y, n_set)
        logger.debug("reduced basin %s, %s: %s", x, y, reduced)
        sizes.append(len(reduced))

    return sizes




def solve(lines):

    logger.info("solve")
    unique_output_counts = 0
    decoded_values = []
    for line in lines:
        logger.info(line)
        
    if PART_1:
        low_points = get_low_points(lines)
        logger.info("Solving part 1")
        # add one to each value and sum
        adjusted_sum =  sum(list(map(lambda x: x + 1, low_points)))
        return adjusted_sum

    basin_sizes = get_basin_sizes(lines)
    value = 1
    top_3 = sorted(basin_sizes)[-3:]
    for x in top_3:
        value *= x
    return value
    
    

    return "part 2"


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.info("Logger init for %s", sys.argv[0])
    year = 2021
    day = 9

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

    # -d just show the data
    if args.print_data:
        for line in lines:
            print(line)
        sys.exit(0)

    print("Wrogin solutions: (5850)")
    print("Solution:", solve(lines=lines))
    print("done.")

# end

