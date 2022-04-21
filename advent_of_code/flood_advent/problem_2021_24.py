"""
    problem_2021_24.py
"""

import pprint
import queue
import re
import sys
import copy
from typing import List, Any, Generator, Iterator
from dataclasses import dataclass
from enum import IntEnum

import itertools
import logging
from flood_advent.utils import line_to_parts
from flood_advent.utils import SparseGrid
from flood_advent.utils import init_logging
from flood_advent.utils import LOGGER_NAME
from flood_advent.utils import binary_list_to_int
from flood_advent.utils import parse_args
from flood_advent.utils import Input

logger = logging.getLogger(LOGGER_NAME)

PART_1 = False



class ALU():

    def __init__(self, lines):
        self.lines = lines
        self.init_reg()


    def __repr__(self):
        return f"w: {self.reg['w']} x: {self.reg['x']} y: {self.reg['y']} z: {self.reg['z']}"

    def init_reg(self):
        self.reg = {
            'w': 0,
            'x': 0,
            'y': 0,
            'z': 0,
        }

    def val_or_var(self, value):
        # logger.info("Val or var for %s", value)
        if value in self.reg:
            # logger.info("returning value in variable %s", value)
            return self.reg[value]
        else:
            # logger.info("returning literal %s", value)
            return int(value)

    def get_registers(self):
        return tuple([self.reg['w'], self.reg['x'], self.reg['y'], self.reg['z']])

    def optimize(self):

        states = {}

        for x in range(111, 999):
            if '0' in str(x):
                continue
            try:
                self.run(str(x), 40)
                reg = self.get_registers()
                states.setdefault(reg, [])
                states[reg].append(x)
            except StopIteration:
                raise
        pprint.pprint(states)

    def run(self, str_input, breakpoint=-1):
        self.init_reg()
        
        def read_input():
            for char in str_input:
                yield int(char)

        inp = read_input()

        for idx, line in enumerate(self.lines):
            if idx == breakpoint:
                return

            args = line.split(' ') 
            # logger.info("args: %s", args)
            inst = args[0]

            if inst == 'inp':
                self.reg[args[1]] = next(inp)
            elif inst == 'add':
                self.reg[args[1]] = self.reg[args[1]] + self.val_or_var(args[2])
            elif inst == 'mul':
                self.reg[args[1]] = self.reg[args[1]] * self.val_or_var(args[2])
            elif inst == 'div':
                self.reg[args[1]] = self.reg[args[1]] // self.val_or_var(args[2])
            elif inst == 'mod':
                # logger.info("Performing mod on %s", self)
                #for k, v in self.reg.items():
                    # logger.info("Type of %s=%s %s %s", k, v, type(k), type(v)) 
                orig = self.reg[args[1]]
                self.reg[args[1]] = self.reg[args[1]] % self.val_or_var(args[2])
            elif inst == 'eql':
                if self.reg[args[1]] == self.val_or_var(args[2]):
                    self.reg[args[1]] = 1
                else: 
                    self.reg[args[1]] = 0
            else:
                raise Exception()
        return  self.reg['z']           

def solve(lines):
    alu = ALU(lines)
    alu.optimize()
    return
    max_14 = None
    for x in range(11111111111111, 11111111999999):
        sx = str(x)
        if '0' not in sx:
            if x % 11111 == 0:
                print(x)
            if not alu.run(sx):
                max_14 = sx
                print("NEw MAX: %s", max_14)

    print(max_14)
    

if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.debug("Logger init")
    year = 2021
    day = 24

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
