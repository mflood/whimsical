"""
    problem_2021_03.py
"""
YEAR=2021
DAY=3

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


def get_counts(lines: List[str]):
    results = [0 for x in range(len(lines[0]))]
    print(results)
    for item in lines:
        for idx, value in enumerate(item):
            if value == "1":
                results[idx] += 1
        print(results)

    return results


def find_keep_value(more_ones: bool, use_most_common: bool):
    if more_ones and use_most_common or not (more_ones or use_most_common):
        return "1"

    return "0"

def scrub(lines: List[str], use_most_common: bool, index: int):

    if len(lines) == 1:
        return lines
    total_items = len(lines)
    total = 0
    for item in lines:
        total += int(item[index])

    more_ones = total >= total_items / 2

    print(f"idx {index}: more_ones: {more_ones}")
    keep = find_keep_value(more_ones=more_ones, use_most_common=use_most_common)
    print(f"keeping {keep}") 

    return_list = [i for i in lines if i[index] == keep]
    print("new return list:")
    for item in return_list:
        print(item)

    return scrub(lines = return_list, use_most_common=use_most_common, index = index +1)


def binary_list_to_int(binary_list: List[str]) -> int:

    # convert to strings
    binary_list = [str(x) for x in binary_list]
    as_string = "".join(binary_list)
    print(as_string)
    as_int= int(as_string, 2)
    print(as_int)
    return as_int



if __name__ == "__main__":

    args = sys.argv

    if len(args) > 1 and args[1] == "test":
        lines = list(get_lines(use_test_data=True))
    else:
        lines = list(get_lines(use_test_data=False))


    ##################### Solution
    counts = get_counts(lines = lines)

    num_lines = len(lines)

    gamma = []
    epsilon = []
    for item in counts:
        if item > num_lines / 2:
            gamma.append("1")
            epsilon.append("0")
        else:
            gamma.append("0")
            epsilon.append("1")

    gamma_int = binary_list_to_int(binary_list=gamma)
    epsilon_int = binary_list_to_int(binary_list=epsilon)
    print(gamma_int * epsilon_int)


    oxygen = scrub(lines, use_most_common=True, index =0)
    co2 = scrub(lines, use_most_common=False, index =0)

    print(f"oxygen: {oxygen}")
    print(f"co2: {co2}")

    o_int = binary_list_to_int(oxygen)
    c_int = binary_list_to_int(co2)

    print(o_int)
    print(c_int)
    print(o_int * c_int)

# end

