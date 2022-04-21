"""
    problem_2021_02.py
"""
from typing import List, Any, Generator, Iterator 
from dataclasses import dataclass
from enum import IntEnum

from itertools import combinations

from flood_advent.utils import get_integers_from_file
from flood_advent.utils import get_input_from_file
from flood_advent.utils import read_comma_separated_ints
from flood_advent.utils import line_to_parts
from flood_advent.utils import SparseGrid


YEAR=2021
DAY=2

def get_file_lines() -> List[Any]:

    INPUT_FILE=f"data/{YEAR}/day/{DAY}/input.txt"
    #line_generator = get_integers_from_file(filepath=INPUT_FILE)
    line_generator = get_input_from_file(filepath=INPUT_FILE)
    return line_generator


def get_test_lines() -> List[Any]:
    test_lines = [
        'forward 5',
        'down 5',
        'forward 8',
        'up 3',
        'down 8',
        'forward 2',
    ]
    return test_lines
    

def get_lines(use_test_data: bool) -> List[Any]:
    if use_test_data:
        return get_test_lines()
    return get_file_lines()

lines = list(get_lines(use_test_data=False))

##################### Solution

@dataclass
class Submarine():
    vert: int = 0
    hor: int = 0
    aim: int = 0

    def get_depth(self):
        return 0 - self.vert

    def process(self, line: str):
        command, val = item.split(' ')
        val = int(val)
        if command== "forward":
            self.hor += val
            adj = self.aim * val
            self.vert -= adj
        elif command== "up":
            #self.vert += val
            self.aim -= val
        elif command== "down":
            #self.vert -= val
            self.aim += val

    def final(self):
        return self.vert * self.hor
        

s = Submarine()
for item in lines:
    s.process(line=item)

print(s)
print(s.final())
# end
