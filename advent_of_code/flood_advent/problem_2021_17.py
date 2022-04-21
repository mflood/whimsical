"""
    problem_2021_17.py
"""

import math
import re
import sys
from typing import List, Any, Generator, Iterator 
from dataclasses import dataclass
import pprint
from enum import IntEnum
import queue

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


def get_range(v1, v2, rev=False):
    a = min(v1, v2)
    b = max(v1, v2)
    value_range = b - a
    ret = []
    for i in range(value_range):
        ret.append(a + i)
    if rev:
        ret.reverse,
    return ret



class Physics():

    def __init__(self, drawx1, drawx2, drawy1, drawy2, x1, x2, y1, y2):
        self.drawx1=drawx1
        self.drawx2=drawx2
        self.drawy1=drawy1
        self.drawy2=drawy2
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.trajectory = []


    def get_possible_yvel(self):
        miny = min(self.y1, self.y2, 0)
        logger.info("miny: %s", miny)
        maxy = max(self.y1, self.y2, 0)
        logger.info("maxy: %s", maxy)
        out_of_bounds = max(abs(miny), abs(maxy))
        logger.info("out of bounds: %s", out_of_bounds)

        ret = []
        max_vel = 200
        out_of_bounds = 200
        for y in range(0, out_of_bounds + 1):
            ret.append(y)

        neg_y = [0-y for y in ret if y != 0]
        ret.extend(neg_y)
        logger.info("Possible y: %s", ret)
        return ret

    def get_possible_xvel(self):
        left_side = min(self.x1, self.x2)
        max_vel = max(self.x1, self.x2) + 1

        min_vel = int(math.sqrt(left_side))

        ret = []
        max_vel = 200
        for x in range(1, max_vel):
            ret.append(x) 
        logger.info("Possible x: %s", ret)
        return ret

    def get_trajectory_height(self):
        y_list = [i[1] for i in self.trajectory]
        max_y = max(y_list)
        logger.debug("found height %d in %s", max_y, y_list)
        return max(y_list)

    def create_trajectory(self, xvel, yvel):
        self.trajectory = []
        x=0
        y=0
        while (x <= max(self.x1, self.x2)) and (y >= min(self.y1, self.y2)):
            x += xvel 
            y += yvel
            xvel = max(0, xvel-1)
            yvel -= 1
            self.trajectory.append((x, y))
        logger.debug("Trajectory: %s", self.trajectory)
        

    def trajectory_hits_target(self) -> bool:
        """
            Return true if tractory hits the target
        """
        for (x, y) in self.trajectory:
            if self.in_target(x, y):
                return True

        return False

    def in_trajectory(self, x, y):
        if (x, y) in self.trajectory:
            return True
        return False

    def in_target(self, x, y):
        if self.y1 <= y and y <= self.y2:
            if self.x1 <= x and x <= self.x2:
                return True

        return False

    def print(self, show_coord=False):
        
        for y in get_range(self.drawy1, self.drawy2, rev=True):
            for x in get_range(self.drawx1, self.drawx2):
                char = "."
                if y == 0 and x == 0:
                    char = "S"

                if self.in_target(x, y):
                    char = 'T'

                if self.in_trajectory(x, y):
                    char = '#'

                if show_coord:
                    val = f"({x}{char}{y})"
                else:
                    val = char
                print(val, end=" ")
            print("")


#def diff(trajectories):
#
#    good = [(23,-10),(25,-9),(27,-5),(29,-6),(22,-6),(21,-7),(9,0),(27,-7),(24,-5),
#    (25,-7),(26,-6),(25,-5),(6,8),(11,-2),(20,-5),(29,-10),(6,3),(28,-7),
#    (8,0),(30,-6),(29,-8),(20,-10),(6,7),(6,4),(6,1),(14,-4),(21,-6),
#    (26,-10),(7,-1),(7,7),(8,-1),(21,-9),(6,2),(20,-7),(30,-10),(14,-3),
#    (20,-8),(13,-2),(7,3),(28,-8),(29,-9),(15,-3),(22,-5),(26,-8),(25,-8),
#    (25,-6),(15,-4),(9,-2),(15,-2),(12,-2),(28,-9),(12,-3),(24,-6),(23,-7),
#    (25,-10),(7,8),(11,-3),(26,-7),(7,1),(23,-9),(6,0),(22,-10),(27,-6),
#    (8,1),(22,-8),(13,-4),(7,6),(28,-6),(11,-4),(12,-4),(26,-9),(7,4),
#    (24,-10),(23,-8),(30,-8),(7,0),(9,-1),(10,-1),(26,-5),(22,-9),(6,5),
#    (7,5),(23,-6),(28,-10),(10,-2),(11,-1),(20,-9),(14,-2),(29,-7),(13,-3),
#    (23,-5),(24,-8),(27,-9),(30,-7),(28,-5),(21,-10),(7,9),(6,6),(21,-5),
#    (27,-10),(7,2),(30,-9),(21,-8),(22,-7),(24,-9),(20,-6),(6,9),(29,-5),
#    (8,-2),(27,-8),(30,-5),(24,-7)]
#    
#    for t in good:
#        if t in trajectories:
#            logger.info("good: %s", t)
#        else:
#            logger.error("missing: %s", t)
#

def solve(lines):

    DRAW = [0, 30, 40, -40]
    for line in lines:
        # target area: x=137..171, y=-98..-73
        # target area: x=137..171, y=-98..-73
        logger.info("Input: %s", line)
        m = re.match(r"target area: x=([-0-9]+)..([-0-9]+), y=([-0-9]+)..([-0-9]+)", line)

        info = {
            "x1": int(m.group(1)),
            "x2": int(m.group(2)),
            "y1": int(m.group(3)),
            "y2": int(m.group(4)),
        }
        logger.info(info)
        p = Physics(DRAW[0], DRAW[1], DRAW[2], DRAW[3], info["x1"], info["x2"], info["y1"], info["y2"])
        max_y = -99
        best_t = None
        trajectories = []
        x_list = p.get_possible_xvel()
        y_list = p.get_possible_yvel()
        for x in x_list:
            for y in y_list:
                logger.debug("Using x vel %s, y vel %s", x, y)
                p.create_trajectory(x, y)
                if p.trajectory_hits_target():
                    trajectories.append((x, y))
                    logger.debug("HIT!!!!!")
                    top = p.get_trajectory_height()
                    if top > max_y:
                        max_y = top
                        best_t = (x, y)
                        logger.debug("BEST HEIGHT %s!!!!!", best_t)
                        p.print,

        #print(trajectories)
        #diff(trajectories)
        return (best_t, max_y, len(trajectories))
    return 0


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.info("Logger init for %s", sys.argv[0])
    year = 2021
    day = 17

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
    print("too low: 1481")
    print("too high: 1566")
    print("done.")

# end

