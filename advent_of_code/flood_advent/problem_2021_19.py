"""
    problem_2021_19.py
"""

import sys
import copy
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

PART_1 = True


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        logger.debug("Created point '%d', '%d', '%d'", self.x, self.y, self.z)

    def __repr__(self):
        return f"({ self.x }, { self.y }, { self.z })"

class Orientation:
    """
    6 possible faces can be facing you
    4 different rotations of each face
    """

    def __init__(self):
        self.center_x = 0
        self.center_y = 0
        self.center_z = 0
        self.face = 0
        self.rotation = 0
    
    def position(self, x, y, z):
        self.center_x = x
        self.center_y = y
        self.center_z = z

    def __repr__(self):
        return f"({self.center_x}, {self.center_y}, {self.center_z}) face: {self.face} rotation: {self.rotation}"

    def convert_point(self, x, y, z):

        # Rubiks cube, red face, yellow top
        if self.face == 0:
            new_x = x
            new_y = y
            new_z = z
        elif self.face == 1:
            # yellow face, orange top
            new_x = x
            new_y = z * -1
            new_z = y
        elif self.face == 2:
            # white face, red top
            new_x = x
            new_y = z  # same
            new_z = y * -1
        elif self.face == 3:
            # orange face, white top
            new_x = x
            new_y = y * -1
            new_z = z * -1
        elif self.face == 4:
            # blue face, yellow top
            new_x = z
            new_y = y
            new_z = x * -1
        elif self.face == 5:
            # green face, yellow top
            new_x = z * -1
            new_y = y
            new_z = x
        else:
            raise Exception()

        x = new_x
        y = new_y
        z = new_z

        for i in range(self.rotation):
            new_x = y
            new_y = x * -1
            x = new_x
            y = new_y

        return (x + self.center_x, y + self.center_y, z + self.center_z)


class Scanner:
    def __init__(self, title):
        logger.debug("Creating scanner '%s'", title)
        self.title = title
        self.orientation = Orientation()
        self._points = []
        self.solved = False

    def add_line(self, data):
        """
        initialization
        """
        coord = data.split(",")
        coord = [int(cc) for cc in coord]
        p = Point(*coord)
        self._points.append(p)

    def get_points(self):
        return_points = []
        for p in self._points:
            x, y, z = self.orientation.convert_point(p.x, p.y, p.z)
            return_points.append((x, y, z))
        return return_points

    def __str__(self):
        ret = self.title
        return ret


class Grid:
    def __init__(self, root_scanner):
        self.scanners = [root_scanner]
        self._all_points = self._get_points()

    def print(self):
        for s in self.scanners:
            print(s.title, s.orientation)

    def get_points(self):
        return self._all_points

    def _get_points(self):
        full_set = []
        for s in self.scanners:
            full_set.extend(s.get_points())
        full_set = set(full_set)
        return full_set

    def get_points_in_range(self, x, y, z):
        """
        Get all points in the grid
        that should be visible to the scanner
        1000 points in all directions
        """

        return_set = []
        for point in self.get_points():
            min_x = x - 1000
            max_x = x + 1000
            if point[0] < min_x or max_x < point[0]:
                continue

            min_y = y - 1000
            max_y = y + 1000
            if point[1] < min_y or max_y < point[1]:
                continue

            min_z = z - 1000
            max_z = z + 1000
            if point[2] < min_z or max_z < point[2]:
                continue
            return_set.append(point)
        return return_set

    def add_scanner(self, scanner):
        logger.info("Trying to merge in scanner %s", scanner)
        grid_points = self.get_points()
        for face in range(6):
            scanner.orientation.face = face
            for rotation in range(4):
                scanner.orientation.rotation = rotation
                scanner.orientation.center_x = 0
                scanner.orientation.center_y = 0
                scanner.orientation.center_z = 0
                scanner_points = scanner.get_points()

                for grid_point in grid_points:
                    for scanner_point in scanner_points:
                        # adjust position of scanner so points are
                        # at the same coordinate given the orientation
                        scanner.orientation.center_x = grid_point[0] - scanner_point[0]
                        scanner.orientation.center_y = grid_point[1] - scanner_point[1]
                        scanner.orientation.center_z = grid_point[2] - scanner_point[2]

                        in_range_points = self.get_points_in_range(
                            scanner.orientation.center_x,
                            scanner.orientation.center_y,
                            scanner.orientation.center_z,
                        )
                        if len(in_range_points) < 12:
                            continue

                        adj_scanner_points = scanner.get_points()

                        matched_points = set(in_range_points) & set(adj_scanner_points)

                        if len(matched_points) >= 12:
                            logger.info("YAY! merged in scanner %s", scanner.title)
                            self.scanners.append(scanner)
                            self._all_points = self._get_points()
                            return True
        return False


def load_scanners(lines):
    """
    Convert input data into scanners

    --- scanner 26 ---
    -291,-599,-618
    -703,734,649
    36,56,-73
    637,871,292
    """

    current_scanner = None
    scanners = []
    for line in lines:
        logger.debug("parsing line: %s", line)
        if not line:
            continue
        if line.find("scanner") > 0:
            logger.debug("Creating scanner for line %s", line)
            scanner_id = line.split(" ")[2]
            scanner = Scanner(title=scanner_id)
            scanners.append(scanner)
        else:
            logger.debug(f"Adding coordinates to scanner {line}")
            scanners[-1].add_line(line)
    return scanners


def process(lines: List[int]):

    scanners = load_scanners(lines=lines)

    grid = Grid(root_scanner=scanners[0])
    unprocessed_scanners = scanners[1:]

    while unprocessed_scanners: 
        scan_these = [x for x in unprocessed_scanners]
        for scanner in scan_these:
            logger.info("Trying to fit scanner %s into grid", scanner.title)
            if grid.add_scanner(scanner):
                unprocessed_scanners.remove(scanner)
                grid.print()

    points = grid.get_points()
    logger.info("Final set of points: %s", points)
    grid.print()
    return len(points)


def solve(lines):

    fuel = process(lines=lines)

    return fuel


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.debug("Logger init")
    year = 2021
    day = 19

    if args.year_day:
        year = int(args.year_day[:4])
        day = int(args.year_day[4:])

    problem_input = Input(year=year, day=day, use_test_data=args.use_test_data)
    lines = problem_input.get_lines()
    # lines  = problem_input.get_floats()
    # lines  = problem_input.get_ints()

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
