"""
    problem_2022_09.py
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

class BridgeMatrix:

    def __init__(self):
        self.head_pos = (0, 0)
        self.tail_pos = (0, 0)
        self.xy_matrix = {(0, 0): 1}

    def get_tail_visit_counts(self):
        total = 0
        for val in self.xy_matrix.values():
            if val:
                total += 1

        return total

    def move_head(self, adjustment_tuple):
        self.head_pos = (self.head_pos[0] + adjustment_tuple[0], self.head_pos[1] + adjustment_tuple[1])
        self.xy_matrix.setdefault(self.head_pos, 0)

        #print(self) 

        # move tail to follow
        x_diff = self.head_pos[0] - self.tail_pos[0]
        y_diff = self.head_pos[1] - self.tail_pos[1]

        if (abs(x_diff) >= 2) or (abs(y_diff) >= 2):
            x_diff = x_diff - int(x_diff / 2.0)
            y_diff = y_diff - int(y_diff / 2.0)
            tail_movement = (x_diff, y_diff)
            self.tail_pos = (self.tail_pos[0] + tail_movement[0], self.tail_pos[1] + tail_movement[1])
            self.xy_matrix.setdefault(self.tail_pos, 0)
            self.xy_matrix[self.tail_pos] += 1
            #print(self)


    def perform_motions(self, motion_string):
        motion_dict = {
        'R': (1, 0),
        'L': (-1, 0),
        'U': (0, 1),
        'D': (0, -1),
        }
        direction, distance = motion_string.split(' ')
        motion = motion_dict[direction]
        for x in range(int(distance)):
            self.move_head(adjustment_tuple=motion)

    def __str__(self):
        ret = ""
        min_x = min(set([v[0] for v in self.xy_matrix]))
        max_x = max(set([v[0] for v in self.xy_matrix]))
        min_y = min(set([v[1] for v in self.xy_matrix]))
        max_y = max(set([v[1] for v in self.xy_matrix]))

        # traverse rows backwards.... 
        y_vals = list(range(min_y, max_y + 1))
        y_vals.reverse()
        for y in y_vals:
            for x in range(min_x, max_x + 1):
                val = self.xy_matrix.get((x, y))
                if (x, y) == self.head_pos:
                    ret += "H"
                elif (x, y) == self.tail_pos:
                    ret += "T"
                elif (x, y) == (0, 0):
                    ret += "s"
                elif val is not None:
                    if val == 0:
                        ret += "-"
                    else:
                        ret += '#'
                else:
                    ret += "."
            ret += "\n"
        return ret


def solve_part_1(lines):

    matrix = BridgeMatrix()
    for line in lines:
        matrix.perform_motions(motion_string=line)
    print(matrix)
    return matrix.get_tail_visit_counts()
    pass

def solve_part_2(lines):

    pass



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
    day = 9

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
