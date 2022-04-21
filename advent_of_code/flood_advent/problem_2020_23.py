"""
    problem_2020_23.py
"""

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

PART_1 = 0


class Cup():

    def __init__(self, cup_id):
        self.cup_id = cup_id
        self.clock_cup = None
        self.counter_cup = None

    def extract(self, number):
        slice_start = self.clock_cup
        current = slice_start
        for x in range(number):
            current = current.clock_cup

        new_clock = current.clock_cup
        new_clock.counter_cup=self
        self.clock_cup = new_clock
        #logger.info("Extracting from %s to %s", slice_start.cup_id, current.cup_id)
        slice_start.counter_cup = None
        current.clock_cup = None
        return slice_start, current

    def get_chained_cups(self):
        current_cup = self
        yield current_cup
        while current_cup:
            current_cup = current_cup.clock_cup
            if not current_cup or current_cup == self:
                return
            yield current_cup

    def print_chain(self):
        current_cup = self
        while current_cup:
            print(current_cup.cup_id, end="")
            current_cup = current_cup.clock_cup
            if not current_cup or current_cup == self:
                print("")
                return

    def insert(self, slice_start, slice_end):

        self.clock_cup.counter_cup = slice_end
        slice_end.clock_cup = self.clock_cup

        self.clock_cup = slice_start
        slice_start.counter_cup = self

    def as_string(self, is_current):

        prev_id = "?"
        if self.counter_cup:
            prev_id = self.counter_cup.cup_id
        next_id = "?"
        if self.clock_cup:
            next_id = self.clock_cup.cup_id
        ret = f"<-({prev_id}) {self.cup_id} ({next_id})->"
        ret = f"{self.cup_id}"
        if is_current:
            ret = f"({ret})"
        return ret


class GameCircle():

    def __init__(self, positions):

        self.cup_map = {}
        self.current_cup = None
        previous_cup = None
        for cup_id in positions:
            cup_id = int(cup_id)
            cup = Cup(cup_id=cup_id)
            self.cup_map[cup_id] = cup

            if not self.current_cup:
                self.current_cup = cup

            if previous_cup:
                cup.counter_cup = previous_cup
                previous_cup.clock_cup = cup

            #print(cup.as_string(is_current = False))
            previous_cup = cup
        previous_cup.clock_cup = self.current_cup
        self.current_cup.counter_cup = previous_cup


    def to_list(self):
        return_list = []
        current_cup = self.current_cup
        while current_cup:
            return_list.append(current_cup)
            current_cup = current_cup.clock_cup
            if not current_cup or current_cup == self.current_cup:
                return return_list


    def iterate(self):
        slice_start, slice_end = self.current_cup.extract(2)

        slice_ids = [cup.cup_id for cup in slice_start.get_chained_cups()]
        # find the next insert cup
        current_id = self.current_cup.cup_id
        consider_id = current_id - 1
        insert_id = None
        while insert_id is None:
            if consider_id == 0:
                consider_id = len(self.cup_map)
            if consider_id in slice_ids:
                consider_id -= 1
            else:
                insert_id = consider_id


        insert_cup = self.cup_map[insert_id]

        #logger.info("destination: %s", insert_cup.cup_id)
        insert_cup.insert(slice_start, slice_end)
        self.current_cup = self.current_cup.clock_cup

    def find_insertion_point(self):

        current_cup = self.current_cup
        while current_cup:
            current_cup = current_cup.clock_cup
            if not current_cup or current_cup == self.current_cup:
                return

    def print_solution(self):
        if PART_1:
            start = self.cup_map[1]
            start.print_chain()
        else:
            cup_1 = self.cup_map[1].clock_cup
            cup_2 = cup_1.clock_cup
            logger.info("%s * %s = %s", cup_1.cup_id, cup_2.cup_id, cup_1.cup_id * cup_2.cup_id)

    def print(self):

        current_cup = self.current_cup
        while current_cup:
            print(current_cup.as_string(current_cup==self.current_cup), end="   ")
            current_cup = current_cup.clock_cup
            if not current_cup or current_cup == self.current_cup:
                print("")
                return


def solve(lines):

    append = 1000000
    starting_positions = [int(a) for a in lines[0]]
    logger.info("Appending values")
    for x in range(max(starting_positions) + 1, append + 1):
        starting_positions.append(x)

    #logger.info("Starting positions: %s", starting_positions)
    logger.info("Starting positions length: %s", len(starting_positions))

    
    logger.info("Creating Game")
    game = GameCircle(positions = starting_positions)

    logger.info("Starting iterations")
    for x in range(10000000):
        game.iterate()

    game.print_solution()


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.info("Logger init for %s", sys.argv[0])
    year = 2020
    day = 23

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

