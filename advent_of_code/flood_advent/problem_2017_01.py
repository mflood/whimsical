"""
    problem_2017_01.py
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


def test_1():
    test = "1122"
    return [x for x in test]

def test_2():
    test = "91212129"
    return [x for x in test]

if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    year = 2017
    day = 1

    if args.year_day:
        year = int(args.year_day[:4])
        day =int(args.year_day[4:])

    problem_input = Input(year=year, day=day, use_test_data=args.use_test_data)
    #lines  = problem_input.get_lines()
    #lines  = problem_input.get_floats()
    #lines  = problem_input.get_ints()

    lines  = problem_input.get_chars()
    lines = list(lines)
    logger.info("Loaded %d values", len(lines))
    
    if args.print_data:
        for line in lines:
            print(line)

        sys.exit(0)

    ##################### Solution

    test_1_input = test_1()
    test_2_input = test_2()
    input_sets = [lines, test_1_input, test_2_input]

    for input_set in input_sets:
        
        chars = list(input_set)
        # wrap the first char
        chars.append(lines[0])
        last = None
        my_sum = 0
        for item in chars:
            if last is None:
                last = item
                continue
            if item  == last:
                my_sum += int(item)
            last = item

        print(my_sum)

# end



