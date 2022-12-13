"""
    problem_2022_05.py
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


class EndOfCratesException(Exception):
    pass


@dataclass
class Crate:
    crate_id: str


@dataclass
class Stack:
    stack_id: int
    crates: List[Crate]


@dataclass
class CargoShip:
    stack_dict: dict[int, Stack]

    def push(self, crates: List[Crate], to_stack: int):
        print(f"pushing {crates} onto stack {to_stack}")
        stack = self.stack_dict[to_stack]
        stack.crates.extend(crates)

    def pull(self, num: int, from_stack: int):
        print(f"pulling {num} from stack {from_stack}")
        stack = self.stack_dict[from_stack]
        print(stack)
        return_stack = []
        for x in range(num):
            crate = stack.crates.pop()
            print(f"popped {crate}")
            return_stack.append(crate)
        return return_stack

    def get_max_height(self):
        max_height = 0
        for stack in self.stack_dict.values():
            height = len(stack.crates)
            if height > max_height:
                max_height = height

        return max_height

    def get_crates_in_row(self, row_from_bottom):
        crate_row = []
        for x in range(len(self.stack_dict)):
            stack = self.stack_dict[x + 1]
            try:
                crate = stack.crates[row_from_bottom]
                crate_row.append(crate)
            except IndexError:
                crate_row.append(None)
        return crate_row

    def get_top_crates(self) -> List[Optional[Crate]]:
        return_list = []
        for x in range(len(self.stack_dict)):
            stack_id = x + 1
            stack = self.stack_dict[stack_id]
            if stack.crates:
                return_list.append(stack.crates[-1])
            else:
                return_list.append(None)

        return return_list

    def print(self):
        height = self.get_max_height()
        for distance_from_top in range(height + 1):
            crate_list = self.get_crates_in_row(height - distance_from_top)
            as_string = ""
            for item in crate_list:
                if item:
                    as_string += "[" + item.crate_id + "] "
                else:
                    as_string += "    "
            print(as_string)

        index_string = ""
        for x in range(len(self.stack_dict)):
            index_string += f" {x+1}  "
        print(index_string)


def extract_crates_from_line(line: str) -> dict[int, Crate]:

    if "[" not in line:
        raise EndOfCratesException()

    print(f"extracting crates from {line}")

    stack_dict = {}
    pos = 0
    stack_number = 1
    while pos < len(line):
        if line[pos] != "[":
            stack_number += 1
            pos += 4
            print(f"empty advancing to {pos} for stack {stack_number}")
        elif line[pos] == "[":
            end = line.find("]", pos)
            crate_id = line[pos + 1 : end]
            stack_dict[stack_number] = Crate(crate_id=crate_id)
            print(f"found create at {pos} for stack {stack_number}")
            pos += 4
            stack_number += 1
        else:
            raise ValueError(pos)

    return stack_dict


def build_ship(lines: List[str]) -> CargoShip:

    stacks = {}
    for line in lines:
        try:
            stack_dict = extract_crates_from_line(line=line)
            for stack_id, crate in stack_dict.items():
                stacks.setdefault(stack_id, Stack(stack_id=stack_id, crates=[]))
                stacks[stack_id].crates.insert(0, crate)
        except EndOfCratesException:
            break

    cargo_ship = CargoShip(stack_dict=stacks)

    return cargo_ship


@dataclass
class Command:
    num_to_move: int
    from_stack: int
    to_stack: int


def get_commands(lines) -> List[Command]:
    in_commaonds = False
    commands = []
    for line in lines:
        if line.startswith("move"):
            match = re.match("move (\d+) from (\d+) to (\d+)", line)
            num_to_move = int(match.groups()[0])
            from_stack = int(match.groups()[1])
            to_stack = int(match.groups()[2])
            command = Command(
                num_to_move=num_to_move, from_stack=from_stack, to_stack=to_stack
            )
            commands.append(command)
    return commands


def run_command(cargo_ship: CargoShip, command: Command):

    crates = cargo_ship.pull(num=command.num_to_move, from_stack=command.from_stack)
    cargo_ship.push(crates=crates, to_stack=command.to_stack)
    cargo_ship.print()


def run_command_9001(cargo_ship: CargoShip, command: Command):

    crates = cargo_ship.pull(num=command.num_to_move, from_stack=command.from_stack)
    crates.reverse()
    cargo_ship.push(crates=crates, to_stack=command.to_stack)
    cargo_ship.print()


def solve_part_1(lines):

    cargo_ship = build_ship(lines=lines)
    print(cargo_ship)
    cargo_ship.print()
    commands = get_commands(lines=lines)
    for command in commands:
        run_command(cargo_ship=cargo_ship, command=command)

    top_crates = cargo_ship.get_top_crates()
    print(top_crates)
    ids = [x.crate_id for x in top_crates if x]
    as_string = "".join(ids)
    return as_string


def solve_part_2(lines):

    print("solving part 2")
    cargo_ship = build_ship(lines=lines)
    print(cargo_ship)
    cargo_ship.print()
    commands = get_commands(lines=lines)
    for command in commands:
        run_command_9001(cargo_ship=cargo_ship, command=command)

    top_crates = cargo_ship.get_top_crates()
    print(top_crates)
    ids = [x.crate_id for x in top_crates if x]
    as_string = "".join(ids)
    return as_string


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
    day = 5

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
