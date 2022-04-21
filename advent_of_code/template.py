"""
    problem_2021_02.py
"""
TEST=True

import sys
from typing import List, Any, Generator, Iterator 
from dataclasses import dataclass
from enum import IntEnum

from itertools import combinations

from flood_advent.utils import get_integers_from_file
from flood_advent.utils import get_input_from_file
from flood_advent.utils import read_comma_separated_ints
from flood_advent.utils import read_comma_separated_values
from flood_advent.utils import line_to_parts
from flood_advent.utils import SparseGrid


YEAR=2021
DAY=3

def _get_file_lines(filepath: str) -> List[Any]:

    line_generator = get_input_from_file(filepath=filepath)
    #line_generator = get_integers_from_file(filepath=filepath)
    #line_generator = read_comma_separated_ints(filepath=filepath)
    #line_generator = read_comma_separated_values(filepath=filepath)
    return line_generator

def get_file_lines() -> List[Any]:

    INPUT_FILE=f"data/{YEAR}/day/{DAY}/input.txt"
    return _get_file_lines(filepath=INPUT_FILE)

def get_test_lines_from_file() -> List[Any]:

    INPUT_FILE=f"data/{YEAR}/day/{DAY}/test-input.txt"
    return _get_file_lines(filepath=INPUT_FILE)


def get_test_lines() -> List[Any]:
    test_lines = [
    ]
    return test_lines
    

def get_lines(use_test_data: bool) -> List[Any]:
    if use_test_data:
        #return get_test_lines()
        return get_test_lines_from_file()
    return get_file_lines()


if __name__ == "__main__":

    args = sys.argv

    if len(args) > 1 and args[1] == "test":
        lines = list(get_lines(use_test_data=True))
    else:
        lines = list(get_lines(use_test_data=False))


    ##################### Solution

    for item in lines:
        print(item)

# end
