"""
    problem_2021_10.py
"""

import sys
from typing import List, Any, Generator, Iterator 
from dataclasses import dataclass
import pprint
from enum import IntEnum

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


opposites = {
    '[': ']',
    '(': ')',
    '{': '}',
    '<': '>',
}

scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
    None: 0
}

def parse_line(line):
    logger.info(line)

    stack = []
    for letter in line:
        if letter in opposites:
            stack.append(opposites[letter])
            continue
        match = stack.pop()
        if match != letter:
            logger.info(match)
            return letter


def get_score(line):
    logger.info(line)


    points = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
    }
    stack = []
    for letter in line:
        if letter in opposites:
            stack.append(opposites[letter])
            continue
        match = stack.pop()
        if match != letter:
            logger.info(match)
            return 0

    score = 0
    if stack:
        stack.reverse()
        for item in stack:
            score *= 5
            score += points[item]

    return score 


def solve(lines):

    unique_output_counts = 0
    decoded_values = []
    for line in lines:
        logger.info(line)
        
    score = 0
    if PART_1:
        for line in lines:
            bad_char = parse_line(line)
            score += scores[bad_char]
    else:
        scores = []
        for line in lines:
            score = get_score(line)
            if score:
                scores.append(score)

        scores.sort()
        logger.debug(scores)
        score = scores[len(scores)//2]
        
        
    return score


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.info("Logger init for %s", sys.argv[0])
    year = 2021
    day = 10

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

    print("Wrogin solutions: (5850)")
    print("Solution:", solve(lines=lines))
    print("done.")

# end

