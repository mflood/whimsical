"""
    problem_2021_14.py
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

PART_1 = 1
STEPS = 40

class Polimerization():

    def __init__(self, starting_template, rules):
        # convert string to list
        self.starting_template = starting_template
        self.template = [x for x in starting_template]
        self.pair_counts = {}
        for x in range(len(starting_template) -1):
            key = starting_template[x] + starting_template[x+1]
            self.pair_counts.setdefault(key, 0)
            self.pair_counts[key] += 1
        self.rules = rules
        self.steps = 0

    def apply(self):

        new_counts = {}
        for k, v in self.pair_counts.items():
            insert = self.rules.get(k)
            if insert:
                head_pair = k[0] + insert
                tail_pair = insert + k[1]
                new_counts.setdefault(head_pair, 0)
                new_counts[head_pair] += v
                new_counts.setdefault(tail_pair, 0)
                new_counts[tail_pair] += v
            else:
                new_counts[k] = v

        self.pair_counts = new_counts
            
        self.steps += 1
        return self.pair_counts

    def score(self):

        letter_counts = {}
        for k, v in self.pair_counts.items():
            letter = k[0]
            letter_counts.setdefault(letter, 0)
            letter_counts[letter] += v

        last_letter = self.starting_template[-1]
        letter_counts.setdefault(last_letter, 0)
        letter_counts[last_letter] += 1

        min_v = None
        max_v = None
        for k, v in letter_counts.items():
            logger.info("%s: %s", k, v)
            if min_v is None:
                min_v = v
                max_v = v
                continue

            min_v = min(min_v, v)
            max_v = max(max_v, v)
        score = max_v - min_v
        logger.info("score: %s", score)



def solve(lines):


    template = lines[0]
    rules = {}
    for line in lines[1:]:
        if not line:
            continue
        pair, _, insert = line.split(' ')    
        rules[pair] = insert

    pprint.pprint(rules)
    p = Polimerization(template, rules)
    
    logger.info("Starting template: %s", template)
    print(p)
    for x in range(STEPS):
        logger.info("Starting step %d", x + 1)
        template = p.apply()

    score = p.score()
    return score


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.info("Logger init for %s", sys.argv[0])
    year = 2021
    day = 14

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

    print("Solution:", solve(lines=lines))
    print("done.")

# end

