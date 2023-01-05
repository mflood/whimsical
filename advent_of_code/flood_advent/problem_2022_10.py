"""
    problem_2022_10.py
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



class CpuObserver:

    def __init__(self, interesting_cycles: List[int]):
        self.interesting_cycles = interesting_cycles
        self.signal_strengths = []
   
    def handle_cycle(self, cycle: int, x_register_value: int):
        print(f"cycle: {cycle}: x: {x_register_value}")
        if cycle in self.interesting_cycles:
            sig = x_register_value * cycle
            self.signal_strengths.append(sig)

    def get_sum(self):
        return sum(self.signal_strengths)



@dataclass
class Cpu:
    x_register: int
    cycle: int
    observer: CpuObserver

    def process_instruction(self, line):

        inst_list = line.strip().split(' ')

        if inst_list[0] == "noop":
            print("noop")
            self.cycle += 1
            self.observer.handle_cycle(self.cycle, self.x_register)
        elif inst_list[0] == "addx":
            value = int(inst_list[1])
            print(f"adding {value}")
            self.cycle += 1
            self.observer.handle_cycle(self.cycle, self.x_register)
            self.x_register += value
            self.cycle += 1
            self.observer.handle_cycle(self.cycle, self.x_register)


def solve_part_1(lines):

    observer = CpuObserver(interesting_cycles =[20, 60, 100, 140, 180, 220])
    cpu = Cpu(x_register=1, cycle=1, observer=observer)
    for line in lines:
        cpu.process_instruction(line=line)
    
    return observer.get_sum()


def solve_part_2(lines):

    return "not implemented"



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
    day = 10

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
