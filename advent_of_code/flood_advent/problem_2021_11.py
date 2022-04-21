"""
    problem_2021_11.py
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

class Grid():

    def __init__(self, lines):
        self.width = len(lines[0])
        self.height = len(lines)
        self.cells = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                value = int(lines[y][x])
                o = Octopus(x=x, y=y, value=value, grid=self)
                row.append(o)
            self.cells.append(row)

    def increment_cells(self):
        for y in range(self.height):
            for x in range(self.width):
                o = self.cells[y][x]
                o.increase()

    def flash(self):
        score = 0
        for y in range(self.height):
            for x in range(self.width):
                o = self.cells[y][x]
                score += o.flash()
        return score


    def did_all_flash(self):
        for y in range(self.height):
            for x in range(self.width):
                o = self.cells[y][x]
                if not o.flashed:
                    return False

        raise Exception("All Flashed")
        
    def reset(self):
        for y in range(self.height):
            for x in range(self.width):
                o = self.cells[y][x]
                o.reset()

    def do_round(self):
        self.increment_cells()
        # self.print()
        score = self.flash()
        self.did_all_flash()
        self.reset()
        return score


    def print(self):
        print("-" * 10)
        for y in range(self.height):
            for x in range(self.width):
                o = self.cells[y][x]
                if o.value  > 9:
                    print('*', end="")
                else:
                    print(o.value, end="")
            print("")
        print("-" * 10)

    def get_neighbors(self, octopus):
        return_values = []
        for y in [-1, 0, 1]:
            y += octopus.y
            if y >= self.height or y < 0:
                continue
            for x in [-1, 0, 1]:
                x += octopus.x
                if x >= self.width or x < 0:
                    continue
                if x == octopus.x and y == octopus.y:
                    continue
                o = self.cells[y][x]
                return_values.append(o)

        return return_values

class Octopus():

    def __init__(self, x, y, value, grid):
        self.value = value
        self.flashed = 0
        self.x = x
        self.y = y
        self.grid = grid

    def __str__(self):
        return "(%d, %d): %d" % (self.x, self.y, self.value)

    def increase(self):
        self.value += 1

    def reset(self):
        self.flashed = 0
        if self.value > 9:
            self.value = 0

    def chain_flash(self, source):

        if self.flashed:
            return 0

        self.value += 1
        logger.debug("increased: %s source: %s", self, source)
        # self.grid.print()
        return self.flash()

    def flash(self):

        if self.flashed:
            return 0

        if self.value > 9:
            logger.debug("flashed: %s", self)
            self.flashed = 1
            for neighbor in self.grid.get_neighbors(self):
                self.flashed += neighbor.chain_flash(source=self)
            return self.flashed

        return 0


def solve(lines):

    rounds = 10000
    score = 0
    if PART_1:
        grid = Grid(lines=lines)
        grid.print()
        print("")
        for x in range(rounds):
            print("step", x + 1)
            score += grid.do_round()
            grid.print()
            
    return score


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.info("Logger init for %s", sys.argv[0])
    year = 2021
    day = 11

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

