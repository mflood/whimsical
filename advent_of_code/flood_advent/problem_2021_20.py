"""
    problem_2021_20.py
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


class MinMax():

    def __init__(self):
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None

    def update(self, x, y):
        if self.min_x is not None:
            self.min_x = min(self.min_x, x)
            self.max_x = max(self.max_x, x)
            self.min_y = min(self.min_y, y)
            self.max_y = max(self.max_y, y)
        else:
            self.min_x = x
            self.max_x = x
            self.min_y = y
            self.max_y = y

    def extra_y_range(self, lextra, textra):
        for y in range(self.min_y - lextra, self.max_y + textra):
            yield y

    def extra_x_range(self, lextra, textra):
        for x in range(self.min_x - lextra, self.max_x + textra):
            yield x

    def y_range(self, add):
        for y in range(self.min_y, self.max_y + add):
            yield y

    def x_range(self, add):
        for x in range(self.min_x, self.max_x + add):
            yield x
    

class Image():

    def __init__(self):

        self.pixelmap = {}
        self.min_max = MinMax()
        self.enhance_cache = {}

    def load_image(self, data):
        for y_idx, row in enumerate(data):
            for x_idx, value in enumerate(row):
                self.add_pixels(x_idx, y_idx, value)        

    def coord(self, x, y):
        return f"{x}:{y}"

    def add_pixels(self, x, y, value):
        assert value in ('.', '#')
        self.min_max.update(x, y)
        c = self.coord(x, y)
        self.pixelmap[c] = value

    def pixel_enhance_index(self, x, y, infinite_char):
        pixels = []
        for yi in [-1, 0, 1]:
            adj_y = y + yi
            for xi in [-1, 0, 1]:
                adj_x = x + xi
                c = self.coord(adj_x, adj_y)
                val = self.pixelmap.get(c, infinite_char)
                pixels.append(val)
        # logger.debug(pixels)
        to_b = {".": "0", "#": "1"}
        binary = [to_b[v] for v in pixels]
        # logger.debug(binary)
        as_int = int("".join(binary), 2)
        # logger.debug(as_int)
        return as_int


    def enhance(self, enhancer, infinite_char):
        logger.info("Enhancing image")
        new_image = Image()
        for y in self.min_max.extra_y_range(lextra=5, textra=5):
            for x in self.min_max.extra_x_range(lextra=5, textra=5):
                p_idx = self.pixel_enhance_index(x, y, infinite_char)
                new_value = enhancer.data[p_idx]
                # logger.debug("enhancer value at position %s: '%s'", p_idx, new_value)
                new_image.add_pixels(x, y, new_value)
        return new_image


    def light_pixel_count(self):
        """
        Count number of light ('#') pixels
        """
        total = 0
        for y in self.min_max.y_range(add=1):
            for x in self.min_max.x_range(add=1):
                c = self.coord(x, y)
                v = self.pixelmap.get(c)
                if v == '#':
                    total += 1
        return total

    def print(self):
        for y in self.min_max.extra_y_range(lextra=5, textra=5):
            for x in self.min_max.extra_y_range(lextra=5, textra=5):
                c = self.coord(x, y)
                v = self.pixelmap.get(c, '.')
                print(v, end="")
            print("")

class Enhancer():

    def __init__(self, data):
        self.data = data
        

    def __repr__(self):
        return self.data 


def solve(lines):

    enhancer = Enhancer(data=lines[0])
    print(enhancer)
    image = Image()
    image.load_image(data=lines[2:])
    image.print()

    for x in range(50):
        logger.info("Enhancment #%d", x + 1)
        infinite_char = '.'
        if x % 2 and enhancer.data[0] == '#':
            infinite_char = '#'
        image = image.enhance(enhancer, infinite_char)

    image.print()
    return image.light_pixel_count()


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.debug("Logger init")
    year = 2021
    day = 20

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
    print("too high: 5959")
    print("too high: 5708")
    print("Solution:", solve(lines=lines))
    print("done.")

# end
