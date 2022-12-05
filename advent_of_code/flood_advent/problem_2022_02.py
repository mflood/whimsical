"""
    problem_2022_02.py
"""

import sys
import copy
from typing import List, Any, Generator, Iterator
from dataclasses import dataclass
from enum import IntEnum, Enum

import itertools
import logging
from flood_advent.utils import line_to_parts
from flood_advent.utils import SparseGrid
from flood_advent.utils import init_logging
from flood_advent.utils import LOGGER_NAME
from flood_advent.utils import binary_list_to_int
from flood_advent.utils import parse_args
from flood_advent.utils import Input

logger = logging.getLogger(LOGGER_NAME)

PART_1 = False

class EmptyException(Exception):
    pass

class BreakException(Exception):
    pass

class RockPaperScissors(IntEnum):
    k_rock = 1
    k_paper = 2
    k_scissors =3
    


def what_beats(rps: RockPaperScissors) -> RockPaperScissors:
    if rps == RockPaperScissors.k_rock:
        return RockPaperScissors.k_paper
    if rps == RockPaperScissors.k_paper:
        return RockPaperScissors.k_scissors
    if rps == RockPaperScissors.k_scissors:
        return RockPaperScissors.k_rock

def what_loses_to(rps: RockPaperScissors) -> RockPaperScissors:
    if rps == RockPaperScissors.k_rock:
        return RockPaperScissors.k_scissors
    if rps == RockPaperScissors.k_paper:
        return RockPaperScissors.k_rock
    if rps == RockPaperScissors.k_scissors:
        return RockPaperScissors.k_paper


def rps_from_letter(abcxyz: str) -> RockPaperScissors:
    logger.info(f"Converting {abcxyz} to RPS")
    lookup =  {
        'A': RockPaperScissors.k_rock,
        'B': RockPaperScissors.k_paper,
        'C': RockPaperScissors.k_scissors,
        'X': RockPaperScissors.k_rock,
        'Y': RockPaperScissors.k_paper,
        'Z': RockPaperScissors.k_scissors,
    }
    return lookup[abcxyz]

def win(a: RockPaperScissors, b: RockPaperScissors) -> bool:
    return (
                (a == RockPaperScissors.k_rock and b == RockPaperScissors.k_scissors)
                or
                (a == RockPaperScissors.k_scissors and b == RockPaperScissors.k_paper)
                or
                (a == RockPaperScissors.k_paper and b == RockPaperScissors.k_rock)
          ) 

@dataclass
class Game:
    opponent: RockPaperScissors
    me: RockPaperScissors

    def score(self):
        shape_score = self.me.value
        if win(self.opponent, self.me):
            print("Oppoent Won")
            return 0 + shape_score
        elif win(self.me, self.opponent):
            print("I Won")
            return 6 + shape_score
        else:
            print("tie")
            return 3 + shape_score

def get_game_from_line(line: str) -> Game:
    line = line.strip()

    o, m = line[0], line[-1]
    opponent = rps_from_letter(o)
    if PART_1:
        me = rps_from_letter(m)
    else:
        if m == 'X':
            # need to lose
            me = what_loses_to(rps=opponent)
        elif m == 'Z':
            # need to win
            me = what_beats(rps=opponent)
        else:
            # tie
            me = opponent

    return Game(opponent=opponent, me=me)

def solve_part_1(lines):

    total = 0
    for line in lines:
        game = get_game_from_line(line=line)
        total += game.score()

    return total

def solve_part_2(lines):
    return None


def solve(lines):
    
    if PART_1:
        return solve_part_1(lines=lines)

    return solve_part_1(lines=lines)
if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.debug("Logger init")
    year = 2022
    day = 2

    if args.year_day:
        year = int(args.year_day[:4])
        day = int(args.year_day[4:])

    problem_input = Input(year=year, day=day, use_test_data=args.use_test_data)
    lines = problem_input.get_lines()
    # lines  = problem_input.get_floats()
    #lines  = problem_input.get_ints()

    # convert from generator to list
    lines = list(lines)
    logger.info("Loaded %d values", len(lines))

    if args.print_data:
        for line in lines:
            print(line)

        sys.exit(0)

    ##################### Solution
    print("Solution:", solve(lines=lines))
    print("done.")

# end
