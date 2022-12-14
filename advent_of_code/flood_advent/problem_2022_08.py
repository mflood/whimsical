"""
    problem_2022_08.py
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
"""
30373
25512
65332
33549
35390 

everything <= gets set to 1
eveerything > adds one
[1, 1, 1, 1, 2, 2, 3, 3, 3, 3]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]



"""
class DistanceTracker:

    def __init__(self):
        self.distances: List[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def reset(self):
        self.distances = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


    def add_tree(self, height):
        for x in range(10):
            if x > height:
                self.distances[x] += 1
            else:
                self.distances[x] = 1

    def get_distance(self, height):
        h = self.distances[height]
        return self.distances[height]

@dataclass
class Tree:
    height: int
    x: int
    y: int
    visible_e: bool = False
    visible_w: bool = False
    visible_n: bool = False
    visible_s: bool = False
    distance_e: int = 0
    distance_w: int = 0
    distance_n: int = 0
    distance_s: int = 0

    @property
    def visible(self):
        return self.visible_e or self.visible_w or self.visible_n or self.visible_s

    @property
    def view_distance(self):
        return self.distance_e * self.distance_w * self.distance_n * self.distance_s

class Grid:

    def __init__(self):

        self.grid = []

    def load_trees(self, lines):
        height = len(lines)
        for y in range(height):
            row = []
            if not lines[y]:
                continue
            for x in range(len(lines[y])):
                tree = Tree(height=int(lines[y][x]), 
                    x=x, y=y)
                row.append(tree)
            self.grid.append(row)
        

    def update_visible(self):

        width = len(self.grid[0])
        height = len(self.grid)
        distance_tracker = DistanceTracker()

        # from the west
        for row in self.grid:
            distance_tracker.reset()
            max_height = 0
            for idx, tree in enumerate(row):
                tree.distance_w = distance_tracker.get_distance(height=tree.height)
                distance_tracker.add_tree(height=tree.height)
                if idx == 0:
                    tree.visible_w = True
                    max_height = tree.height
                else:
                    if tree.height > max_height:
                        tree.visible_w = True
                        max_height = tree.height

        # from the east
        for row in self.grid:
            distance_tracker.reset()
            row.reverse()
            max_height = 0
            for idx, tree in enumerate(row):
                tree.distance_e = distance_tracker.get_distance(height=tree.height)
                distance_tracker.add_tree(height=tree.height)
                if idx == 0:
                    tree.visible_e = True
                    max_height = tree.height
                else:
                    if tree.height > max_height:
                        tree.visible_e = True
                        max_height = tree.height
            row.reverse()

        # from the north
        for x in range(width):
            distance_tracker.reset()
            max_height = 0
            for y in range(height):
                tree = self.grid[y][x]
                tree.distance_n = distance_tracker.get_distance(height=tree.height)
                distance_tracker.add_tree(height=tree.height)
                if y == 0:
                    tree.visible_n = True
                    max_height = tree.height
                else:
                    if tree.height > max_height:
                        tree.visible_n = True
                        max_height = tree.height

        # from the south
        for x in range(width):
            distance_tracker.reset()
            max_height = 0
            for y in range(height):
                tree = self.grid[height - y - 1][x]
                tree.distance_s = distance_tracker.get_distance(height=tree.height)
                distance_tracker.add_tree(height=tree.height)
                if height - y == width:
                    tree.visible_s = True
                    max_height = tree.height
                else:
                    if tree.height > max_height:
                        tree.visible_s = True
                        max_height = tree.height


    def max_distance(self) -> int:
        max_d = 0
        for row in self.grid:
            for tree in row:
                if tree.view_distance > max_d:
                    max_d = tree.view_distance
        return max_d

    def num_visible_trees(self):
        total = 0
        for row in self.grid:
            for tree in row:
                if tree.visible:
                    total += 1

        return total

    def __str__(self):
        ret = ""
        for row in self.grid:
            height_string = "".join([str(t.height) for t in row])
            ret += height_string + "\n"
        ret += "\n"

        for row in self.grid:
            string = ''
            for tree in row:
                if tree.visible_w:
                    string += '+'
                else:
                    string += "."
            ret += string + "\n"
        ret += "\n"

        for row in self.grid:
            string = ''
            for tree in row:
                if tree.visible_e:
                    string += '+'
                else:
                    string += "."
            ret += string + "\n"
        ret += "\n"

        for row in self.grid:
            string = ''
            for tree in row:
                if tree.visible_n:
                    string += '+'
                else:
                    string += "."
            ret += string + "\n"
        ret += "\n"

        for row in self.grid:
            string = ''
            for tree in row:
                if tree.visible_s:
                    string += '+'
                else:
                    string += "."
            ret += string + "\n"
        ret += "\n"

        for row in self.grid:
            string = ''
            for tree in row:
                if tree.visible:
                    string += '+'
                else:
                    string += "."
            ret += string + "\n"
        ret += "\n"

        for row in self.grid:
            string = ''
            for tree in row:
                string += str(tree.view_distance)
                string += " "
            ret += string + "\n"
        ret += "\n"

        return ret
    

def solve_part_1(lines):

    grid = Grid()
    grid.load_trees(lines)
    grid.update_visible()
    #print(grid)
    return grid.num_visible_trees()

def solve_part_2(lines):

    grid = Grid()
    grid.load_trees(lines)
    grid.update_visible()
    #print(grid)
    return grid.max_distance()



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
    day = 8

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
