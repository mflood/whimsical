"""
    problem_2022_07.py
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


@dataclass
class File:
    parent: Any
    name: str
    size: int

    def print(self, indent):
        line = " " * indent
        line += f"- {self.name} (file, size={self.size})"
        print(line)


@dataclass
class Directory:
    parent: Any
    name: str
    dirs: List[Any]
    files: List[File]
    cached_size = None

    def print(self, indent):
        line = " " * indent
        line += f"- {self.name or '/'} (dir)"
        print(line)
        for d in self.dirs:
            d.print(indent=indent + 2)

        for f in self.files:
            f.print(indent=indent + 2)

    def pwd(self):
        if self.parent:
            return f"{self.parent.name.rstrip('/')}/{self.name}"
        return "/"

    def total_of_dir_sizes(self, maxi):
        total = 0
        my_size = self.size()
        if my_size <= maxi:
            total += my_size
        for d in self.dirs:
            total += d.total_of_dir_sizes(maxi=maxi)
        return total

    def size(self) -> int:
        if self.cached_size is not None:
            return self.cached_size

        total = 0
        for d in self.dirs:
            total += d.size()
        for f in self.files:
            total += f.size

        self.cached_size = total
        return total


class Session:
    def __init__(self):
        self.root = Directory(parent=None, name="/", dirs=[], files=[])
        self.current_directory = self.root

    def tree(self):
        self.root.print(indent=0)

    def cd(self, new_dir):
        if new_dir == "/":
            self.current_directory = self.root
        elif new_dir == "..":
            self.current_directory = self.current_directory.parent
        else:
            for d in self.current_directory.dirs:
                if d.name == new_dir:
                    self.current_directory = d
                    break
        print(f"cwd is now {self.current_directory.pwd()}")

    def process(self, line):
        line = line.strip()
        print(f"processing {line}")
        if line.startswith("$ ls"):
            return

        if line.startswith("$ cd"):
            new_dir = line.replace("$ cd ", "")
            self.cd(new_dir=new_dir)
            return

        if line.startswith("dir "):
            dir_name = line.replace("dir ", "")
            new_dir = Directory(
                parent=self.current_directory, name=dir_name, dirs=[], files=[]
            )
            self.current_directory.dirs.append(new_dir)
            return

        size, filename = line.strip().split(" ")
        new_file = File(parent=self.current_directory, name=filename, size=int(size))
        self.current_directory.files.append(new_file)


def solve_part_1(lines):

    session = Session()

    for command in lines:
        session.process(command)
    session.tree()
    return session.root.total_of_dir_sizes(maxi=100000)


def solve_part_2(lines):

    return solve_part_1(lines=lines)
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
    day = 7

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
