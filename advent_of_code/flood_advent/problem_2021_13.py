"""
    problem_2021_13.py
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

PART_1 = 1


class Paper():

    def __init__(self):
        self.cell_dict = {}
        self.width = 0
        self.height = 0

    def coord(self, x, y):
        return(f"{x}:{y}")

    def merge_cols(self, x1, x2):
        """     
            merge values of x1 into x2
        """
        logger.debug("merging row %s into row %s", x1, x2)
        for y in range(self.height):
            source = self.cell_dict.get(self.coord(x1, y))
            target = self.cell_dict.get(self.coord(x2, y))
            if source and not target:
                self.add_point(x2, y, source)

    def merge_rows(self, y1, y2):
        """     
            merge values of y1 into y2
        """
        logger.debug("merging row %s into row %s", y1, y2)
        for x in range(self.width):
            source = self.cell_dict.get(self.coord(x, y1))
            target = self.cell_dict.get(self.coord(x, y2))
            logger.debug("%s: (%s, %s) %s -> %s", x, x, y1, source, target)
            if source and not target:
                logger.debug("new point: %s, %s", x, y2)
                self.add_point(x, y2, source)

    def fold_x(self, x):
        for idx, source_x in enumerate(range(x + 1, self.width)):
            target_x = x - (idx + 1)
            self.merge_cols(source_x, target_x)
        self.width = x

    def fold_y(self, y):
        for idx, source_y in enumerate(range(y + 1, self.height)):
            target_y = y - (idx + 1)
            self.merge_rows(source_y, target_y)
        self.height = y

    def process_fold(self, axis, value):
        logger.info("fold '%s', '%s'", axis, value)
        if axis == "x":
            self.fold_x(value)
        else:
            self.fold_y(value)

    def add_lines(self, lines):
        populating = True
        for line in lines:
            if not line:
                populating = False
                continue
            if not populating:
                line = line.replace('fold along ', '')
                axis, value = line.split('=')
                self.process_fold(axis, int(value))
            else:    
                x, y = line.split(',')
                x, y, = int(x), int(y)
                self.add_point(x, y, '#')


    def add_point(self, x, y, value):
        self.width = max(self.width, x + 1)
        self.height = max(self.height, y + 1)

        coordinate = f"{x}:{y}"
        self.cell_dict[coordinate] = value


    def print(self):
        print("-" * self.width)
        dots = 0
        for y in range(self.height):
            print(f"{y}: ", end="")
            for x in range(self.width):
                coordinate = f"{x}:{y}"
                value = self.cell_dict.get(coordinate)
                if not value:
                    print(" ", end='')
                else:
                    dots += 1
                    #print(f"({x}, {y}", end='')
                    print(value, end='')

            print("")
        logger.info("%s dots!", dots)
                

def solve(lines):

    paper = Paper()
    paper.add_lines(lines)
    paper.print()
    return 0


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.info("Logger init for %s", sys.argv[0])
    year = 2021
    day = 13

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

    print("Solution:", solve(lines=lines))
    print("done.")

# end

