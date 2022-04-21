"""
    problem_2021_04.py
"""

import sys
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



class RowSolvedException(Exception):
    pass

class ColumnSolvedException(Exception):
    pass

@dataclass
class BingoSpace():
    value: int
    solved: bool = False

    def __str__(self):
        if self.solved:
            return " *"
        else:
            return f"{ str(self.value).rjust(2) }"

    def get_score(self) -> int:
        if self.solved:
            return 0
        else:
            return self.value
        

class BingoBoard():

    def __init__(self):
        self.rows = []
        self.raw_cells = {}
        self._logger = logging.getLogger(LOGGER_NAME)
        self.solved = False

    def add_row(self, raw_line):
        raw_line = raw_line.replace('  ', ' ')
        self._logger.debug("Adding row: '%s'", raw_line) 
        values = [int(x) for x in raw_line.split(' ')]
        new_row = [] 
        for number in values:
            bingo_space = BingoSpace(value=number)
            new_row.append(bingo_space)
            self.raw_cells[number] = bingo_space

        self.rows.append(new_row)

    def get_score(self, last_number: int):
        total = 0
        for key, cell in self.raw_cells.items():
            total += cell.get_score()
        return total * last_number

    def print(self):
        for row in self.rows:
            print(" ".join( [str(cell) for cell in row] ))

    def test_solved(self):
        for row in self.rows:
            row_solved = True
            for cell in row:
                if not cell.solved:
                    row_solved = False
                    
            if row_solved:
                self.solved = True
                raise RowSolvedException()

        width = len(self.rows[0])
        height = len(self.rows)
        for x in range(width):
            col_solved = True
            for y in range(height):
                cell = self.rows[y][x]
                if not cell.solved:
                    col_solved = False
            if col_solved:
                self.solved = True
                raise RowSolvedException()
                

    def play_number(self, number: int):
        if number in self.raw_cells:
            self.raw_cells[number].solved = True
            self.test_solved()


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.info("Logger init")
    year = 2021
    day = 4

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

    bingo_numbers = lines[0]

    bingo_boards = []
    current_board = None
    for line in lines[1:]:
        if not line:
            if current_board:
                logger.info("finished board")
                bingo_boards.append(current_board)
            logger.info("Creating new board")
            current_board = BingoBoard()
            continue

        current_board.add_row(line)

    if current_board not in bingo_boards:
        bingo_boards.append(current_board)


    for number in lines[0].split(','):
        number = int(number)
        for b in bingo_boards:
            if b.solved:
                continue

            try:
                b.play_number(number=number)
                b.print()
            except (RowSolvedException, ColumnSolvedException) as error:
                logger.info("Winning Board!")
                b.print()
                score = b.get_score(last_number=number)
                print("board score: ", score)

            print("-"* 100)
        

# end

