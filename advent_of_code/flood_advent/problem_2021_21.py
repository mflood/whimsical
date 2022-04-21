"""
    problem_2021_21.py
"""

import sys
import copy
from typing import List, Any, Generator, Iterator
from dataclasses import dataclass
from enum import IntEnum

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

PART_1 = True

class EmptyException(Exception):
    pass

class BreakException(Exception):
    pass


class Die():

    def __init__(self):
        self.current_value = 1
        self.num_rolls = 0

    def roll_quantum(self) -> [int, int]:
        """
        return (total_moves, number_of_instances)
        """
        possibles = itertools.product([1, 2, 3], [1, 2, 3], [1, 2, 3])
        uniques = {}
        for x in possibles:
            total = sum(x)
            uniques.setdefault(total, 0)
            uniques[total] += 1

        for roll, count in uniques.items():
            yield roll, count
        

    def roll(self):
        ret = self.current_value
        self.current_value += 1
        if self.current_value > 100:
            self.current_value = 1
        self.num_rolls += 1
        return ret

class Player():

    def __init__(self, name, start_position):
        self.name = name
        self.moves = 0
        self.quantum_games = {(start_position, 0): 1}
        self.num_wins = 0

    def __repr__(self):
        return f"{self.name} {self.num_wins} wins.  {self.quantum_games}"

    def move_quantum_and_score(self, quantum_rolls):
        print("")
        print("")
        logger.info("Moving %s", self.name) 
        num_wins = 0
        num_under_21 = 0
        new_positions = {}
        for k, num_games in self.quantum_games.items():

            # spot 3, score 15, 10 games
            position, starting_score = k
            logger.debug("Starting from current quantum: position: %d score: %s (%d games)", position, starting_score, num_games)
            for (roll, count) in quantum_rolls:
                # roll 6 (7 instances)
                logger.debug("performing roll %s (%d times)", roll, count)
                # new position = 3 + 6 => 9
                new_position = ((position + roll - 1) % 10) + 1
                # score is 15 + 9 == 24
                score = starting_score + new_position
                if score >= 21:
                    # win and discard
                    # wins = 7 rolls * num_games = 70
                    wins = count * num_games
                    logger.debug("recording %d wins", wins)
                    num_wins += wins
                else:
                    num_under_21 += count * num_games
                    # 10 games * 7 instances have position 1 with score 16  (1, 16)
                    logger.debug("Adding %d games to new_position %s", num_games * count, (new_position, score))
                    new_positions.setdefault((new_position, score), 0) 
                    new_positions[(new_position, score)] += count * num_games
                    logger.debug(new_positions)

        self.quantum_games = new_positions    
        logger.info(self)
        logger.info("after all dice rolls: %s %d wins %d under 21", self.name, num_wins, num_under_21)

        if not num_wins + num_under_21:
            raise EmptyException("No more moves")
        logger.info("Returning %s, %s", num_wins, num_under_21) 
        return num_wins, num_under_21



class Game():

    def __init__(self, p1, p2, die):
        self.p1 = p1
        self.p2 = p2
        self.die = die

    def print(self):
        for x in range(1, 11):
            print(f"{x}: {self.board[x]}")

    def play(self):

        quantum_rolls = list(self.die.roll_quantum())

        last_num_to_lose = 0
        while True:
            for player in [self.p1, self.p2]:
                print("*" * 100)
                logger.info("Starting %s turn: ", player)
                try:
                    num_wins, num_to_lose = player.move_quantum_and_score(quantum_rolls)
                    adjustment = num_wins * last_num_to_lose
                    logger.info("Adding %d to current player.num_wins (%d)", adjustment, player.num_wins)
                    player.num_wins += adjustment
                    last_num_to_lose = num_to_lose
                    logger.info("Set last_num_to_lose to %d", last_num_to_lose) 
                    logger.info("Current player state: %s", player)
                except EmptyException as e:
                    print(self.p1)
                    print(self.p2)
                    raise

def solve(lines):
    p1_start = int(lines[0].split(' ')[-1])
    p2_start = int(lines[1].split(' ')[-1])

    p1 = Player("Player 1", p1_start)
    p2 = Player("Player 2", p2_start)

    die = Die()
    g = Game(p1, p2, die)
    g.play()
    return 0

if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.debug("Logger init")
    year = 2021
    day = 21

    if args.year_day:
        year = int(args.year_day[:4])
        day = int(args.year_day[4:])

    problem_input = Input(year=year, day=day, use_test_data=args.use_test_data)
    lines = problem_input.get_lines()
    # lines  = problem_input.get_floats()
    # lines  = problem_input.get_ints()

    # convert from generator to list
    lines = list(lines)
    logger.info("Loaded %d values", len(lines))

    if args.print_data:
        for line in lines:
            print(line)

        sys.exit(0)

    ##################### Solution
    print("too high: 5959")
    print("too high: 5708")
    print("Solution:", solve(lines=lines))
    print("done.")

# end
