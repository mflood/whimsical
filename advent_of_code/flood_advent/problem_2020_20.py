"""
    problem_2021_06.py
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

class EdgeSide(IntEnum):
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4

class Square():

    def __init__(self, title):
        self.title = title
        self._lines = []
        self.solved = False

    def add_line(self, data):
        """
            initialization
        """
        self._lines.append(data)

    def flip(self):
        self._lines = list(reversed(self._lines))

    def rotate(self):
        
        new_array = []
        for x in range(len(self._lines[0])):
            column = "".join(reversed([row[x] for row in self._lines]))
            new_array.append(column)
        self._lines = new_array

    def get_print_lines(self):
        return self._lines

    def get_top_edge(self):
        return self._lines[0],

    def get_bottom_edge(self):
        return self._lines[-1],
        
    def get_left_edge(self):
        return "".join( [x[0] for x in self._lines] ),

    def get_right_edge(self):
        return "".join( [x[-1] for x in self._lines] ),

    def __str__(self):
        ret = self.title
        ret += "\n-----------\n"
        ret += "\n".join(self._lines)
        ret += "\n-----------\n"
        return ret


class Grid():
    def __init__(self):
        self.grid = {}
        self.squares = {}

    def add_square(self, x, y, square):
        key = f"{x}:{y}"
        self.grid[key] = copy.copy(square)
        self.squares[square.title] = key

    def is_available(self, x, y):

        if f"{x}:{y}" in self.grid:
            return False

        if f"{x+1}:{y}" in self.grid:
            return True

        if f"{x-1}:{y}" in self.grid:
            return True

        if f"{x}:{y+1}" in self.grid:
            return True

        if f"{x}:{y-1}" in self.grid:
            return True

        return False

    def square_fits(self, x, y, square):

        key = f"{x+1}:{y}"
        o_square = self.grid.get(key)
        if o_square:
            if square.get_right_edge() != o_square.get_left_edge():
                return False

        key = f"{x-1}:{y}"
        o_square = self.grid.get(key)
        if o_square:
            if square.get_left_edge() != o_square.get_right_edge():
                return False
        
        key = f"{x}:{y-1}"
        o_square = self.grid.get(key)
        if o_square:
            if square.get_top_edge() != o_square.get_bottom_edge():
                return False

        key = f"{x}:{y+1}"
        o_square = self.grid.get(key)
        if o_square:
            if square.get_bottom_edge() != o_square.get_top_edge():
                return False

        return True


    def get_empty_coordinates(self):
        x_list = []
        y_list = []
        for key in self.grid.keys():
            x, y = key.split(":")
            x_list.append(int(x))
            y_list.append(int(y))

        min_y = min(y_list)
        max_y = max(y_list)
        min_x = min(x_list)
        max_x = max(x_list)

        available_coordinates = []
        for y in range(min_y - 1, max_y + 2): 
            for x in range(min_x - 1, max_x + 2):
                if self.is_available(x, y):
                    available_coordinates.append([x,y])

        return available_coordinates

    def get_corners(self):
        x_list = []
        y_list = []
        for key in self.grid.keys():
            x, y = key.split(":")
            x_list.append(int(x))
            y_list.append(int(y))

        min_y = min(y_list)
        max_y = max(y_list)
        min_x = min(x_list)
        max_x = max(x_list)

        return_list = [
        int(self.grid.get(f"{min_x}:{max_y}").title),
        int(self.grid.get(f"{max_x}:{max_y}").title),
        int(self.grid.get(f"{min_x}:{min_y}").title),
        int(self.grid.get(f"{max_x}:{min_y}").title),
        ]

        return return_list


    def print_titles(self):
        x_list = []
        y_list = []
        for key in self.grid.keys():
            x, y = key.split(":")
            x_list.append(int(x))
            y_list.append(int(y))

        min_y = min(y_list)
        max_y = max(y_list)
        min_x = min(x_list)
        max_x = max(x_list)
        for y in range(min_y, max_y + 1):
            print_row = []
            for x in range(min_x, max_x + 1):
                key = f"{x}:{y}"
                square = self.grid.get(key)
                if not square:
                    print(" ----", end=" ")
                else:
                    print(f" {square.title}", end=" ")
                
            print(" ")
        

    def print(self, cell_size):
        x_list = []
        y_list = []
        for key in self.grid.keys():
            x, y = key.split(":")
            x_list.append(int(x))
            y_list.append(int(y))

        min_y = min(y_list)
        max_y = max(y_list)
        min_x = min(x_list)
        max_x = max(x_list)
        for y in range(min_y, max_y + 1):
            print_row = []
            for x in range(min_x, max_x + 1):
                key = f"{x}:{y}"
                print_row.append(self.grid.get(key))
            
            for cell_y in range(cell_size):
                for item in print_row:
                    if not item:
                        print(" " * cell_size, end=" ")
                    else:
                        print(item.get_print_lines()[cell_y], end=" ")
                
                print(" ")
            print(" ")
        

def recursive_solve(squares, grid):

    unsolved_squares = False
    for square in squares:
        if square.title not in grid.squares:
            unsolved_squares = True
            possible_coordinates = grid.get_empty_coordinates()
            #logger.info("Available coordinates: %s", possible_coordinates)
            for x, y in possible_coordinates:
                for flip in range(2):
                    for rotate in range(4):
                        square.rotate()
                        if grid.square_fits(x, y, square):
                            grid_copy = copy.copy(grid)
                            grid_copy.add_square(x, y, square)
                            #grid.print(cell_size = 10)
                            results = recursive_solve(squares, grid_copy)
                    square.flip()
                    

    if unsolved_squares:
        return None
    return squares

def process(input_list: List[int]):

    logger.info("initial state: %s", input_list)
    
    current_square = None

    squares = []
    for line in input_list:
        print("line: ", line)
        if not line:
            continue
        if line.startswith("Tile"):
            print("Creating square")
            tile_id = line.split(' ')[-1].strip(":")
            square = Square(title=tile_id)
            squares.append(square)
        else:
            print(f"Adding line {line}")
            squares[-1].add_line(line)

    grid  = Grid()
    grid.add_square(0, 0, squares[0])

    solved_grid = recursive_solve(squares, grid)
    grid.print(cell_size = 10)
    grid.print_titles()

    x = 1
    for value in grid.get_corners():
        x *= value
    return x


def solve(lines):

    fuel = process(input_list=lines)

    return fuel

if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.debug("Logger init")
    year = 2020
    day = 20

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

    if args.print_data:
        for line in lines:
            print(line)

        sys.exit(0)

    ##################### Solution

    print("Solution:", solve(lines=lines))
    print("done.")

# end

