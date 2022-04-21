"""
    problem_2019_02.py
"""
from typing import List, Any, Generator, Iterator
from enum import IntEnum

from dataclasses import dataclass
from itertools import combinations

from flood_advent.utils import get_integers_from_file
from flood_advent.utils import get_input_from_file
from flood_advent.utils import read_comma_separated_ints
from flood_advent.utils import line_to_parts
from flood_advent.utils import SparseGrid


YEAR = 2019
DAY = 2


def get_file_lines() -> List[Any]:

    INPUT_FILE = f"data/{YEAR}/day/{DAY}/input.txt"
    # line_generator = get_integers_from_file(filepath=INPUT_FILE)
    # line_generator = get_input_from_file(filepath=INPUT_FILE)
    line_generator = read_comma_separated_ints(filepath=INPUT_FILE)
    return line_generator


def get_test_lines() -> List[Any]:
    as_string = "1,9,10,3,2,3,11,0,99,30,40,50"
    test_values = as_string.split(",")
    test_values = [int(x) for x in test_values]
    return test_values


def get_lines(use_test_data: bool) -> List[Any]:
    if use_test_data:
        return get_test_lines()
    return get_file_lines()


lines = list(get_lines(use_test_data=True))
print(lines)


class HaltException(Exception):
    pass

@dataclass
class Command:
    op: int
    p1: int
    p2: int
    out: int

    def add(self, my_list):
        return my_list[self.p1] + my_list[self.p2]

    def mult(self, my_list):
        return my_list[self.p1] * my_list[self.p2]

    def exec(self, my_list):
        if self.op == 1:
            return self.add()
        elif self.op == 2:
            return self.mult()
        elif self.op == 99:
            raise HaltException()


def get_command(lines, idx) -> Command:
    c = Command(op=lines[idx], p1=lines[idx + 1], p2=lines[idx + 2], out=lines[idx + 3])
    return c


idx = 0
try:
    while idx < len(lines):

        c = get_command(lines, idx)

        print(c)
        val = c.exec()
        lines[c.out] = val

        idx += 4
except Exception:

    print(lines)



# end
