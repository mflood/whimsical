"""
    problem_2021_08.py
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

PART_1 = False

legit = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg'
}

legit_rev = {}
for k, v in legit.items():
    legit_rev[v] = k;


class SignalDriver:
    """
        mapping[me] -> legit signal 
        reverse_mapping[legit signal[ -> mapping 
    """

    def __init__(self):

        self.mapping = {}
        self.reverse_mapping = {}

    def add_mapping(self, driver_letter, legit_letter):
        self.mapping[driver_letter] = legit_letter
        self.reverse_mapping[legit_letter] = driver_letter

    def vanilla(self):  
        for value in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
            self.mapping[value] = value
            self.reverse_mapping[value] = value

    def infer_mapping(self, value_list):
        """
        """
        possible_dict = {}
        for x in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
            possible_dict[x] = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

        #logger.info("starting possible_dict")
        #pprint.pprint(possible_dict)

        def get_matching_legit_words(word):
            possibles = []
            for v in legit.values():
                if len(v) == len(word):
                    possibles.append(v)
            return possibles

        def remove_where_not_match(possible_dict, letters_to_remove):
            for k, v in possible_dict.items():
                if set(v) == set(letters_to_remove):
                    logger.debug("Skipping %s", v)
                    continue

                new_v = list(set(v) - set(letters_to_remove))
                possible_dict[k] = new_v

        for value in value_list:
            """
                value = abcde
                possibles = acdeg, acdfg, abdfg
                letter_set = a, b, c, d, e, f, g
            """
            possibles = get_matching_legit_words(value)
            logger.debug("possibles for %s: %s", value, possibles)
            letter_set = []
            for word in possibles:
                for letter in word:
                    if letter not in letter_set:
                        letter_set.append(letter)
            for letter in value:
                # new possible values are the intersection of the two lists
                possible_dict[letter] = list(set(letter_set) & set(possible_dict[letter]))
                # get rid of letters in possible_dict that are not in letter_set
                    
            logger.debug("letter_set for %s: %s", value, letter_set)


        #logger.info("new possible_dict")
        #pprint.pprint(possible_dict)

        # possible set has been reduced:
        # 'a': ['f', 'c', 'b', 'd'],
        # 'b': ['c', 'g', 'a', 'd', 'f', 'b', 'e'],
        # 'c': ['f', 'c', 'a'],
        # 'd': ['c', 'g', 'a', 'd', 'f', 'b', 'e'],
        # 'e': ['f', 'c', 'b', 'd'],
        # 'f': ['f', 'c'],
        # 'g': ['f', 'c']

        # find value with two elements - segments c and f
        cf_segments = [v for v in possible_dict.values() if len(v) == 2][0]
        remove_where_not_match(possible_dict, cf_segments)
        #pprint.pprint(possible_dict)

        # find other value with two elements - segments b and d
        bd_segments = [v for v in possible_dict.values() if (len(v) == 2 and set(v) != set(cf_segments))][0]
        remove_where_not_match(possible_dict, bd_segments)

        # value with one element is a
        a_segment = [v for v in possible_dict.values() if len(v) == 1][0]
        remove_where_not_match(possible_dict, a_segment)

        # distinguish between f and c
        cf_letters = [k for k, v in possible_dict.items() if set(v) == set(cf_segments)]        
        for letter in cf_letters:
            occurences = 0
            for word in value_list:
                if letter in word:
                    occurences += 1
            if occurences == 9:
                possible_dict[letter] = 'f'
            else:
                possible_dict[letter] = 'c'
                
        # distinguish between b and d
        db_letters = [k for k, v in possible_dict.items() if set(v) == set(bd_segments)]        
        for letter in db_letters:
            occurences = 0
            for word in value_list:
                if letter in word:
                    occurences += 1
            if occurences == 6:
                possible_dict[letter] = 'b'
            else:
                possible_dict[letter] = 'd'

        # find g and e        
        ge_letters = [k for k, v in possible_dict.items() if set(v) == set(["g", "e"])]        
        for letter in ge_letters:
            occurences = 0
            for word in value_list:
                if letter in word:
                    occurences += 1
            if occurences == 7:
                possible_dict[letter] = 'g'
            else:
                possible_dict[letter] = 'e'
        
        # fix a
        a = [k for k, v, in possible_dict.items() if set(v) == set(["a"])][0]
        possible_dict[a] = 'a'
        # pprint.pprint(possible_dict)

        # assign the mapping
        self.mapping = possible_dict
        for k, v in self.mapping.items():
            self.reverse_mapping[v] = k


    def get_numbers(self, input_strings):
        """
            for vanilla: 
            input_strings: ["acdfg", "bcdf", "abdfg", "abdefg"]
            output: [2, 3, 4, 5]
        """
        return_numbers = []
        for string in input_strings:
            legit_signals = []
            for letter in string:
                legit_signals.append(self.mapping[letter])
            legit_key = "".join(sorted(legit_signals))
            return_numbers.append(legit_rev[legit_key])

        return return_numbers


def solve(lines):

    unique_output_counts = 0
    decoded_values = []
    for line in lines:
        logger.debug(line)
        tokens = line.split(' ')
        inputs = tokens[:10]
        outputs = tokens[11:]

        logger.debug("inputs: %s", inputs)
        logger.debug("outputs: %s", outputs)
        
        # order the signals
        inputs = ["".join(sorted(item)) for item in inputs]
        outputs = ["".join(sorted(item)) for item in outputs]

        digit_counts = {}
        for item in inputs:
            l = len(item)
            digit_counts.setdefault(l, [])
            digit_counts[l].append(item)

        #pprint.pprint(digit_counts)
    
        uniques = []
        for signals in digit_counts.values():
            if len(signals) == 1:
                uniques.append(signals[0])

        for item in outputs:
            if item in uniques:
                unique_output_counts += 1

        sg = SignalDriver()
        sg.infer_mapping(inputs)
        numbers = sg.get_numbers(outputs)
        logger.debug(numbers)
        decoded = int("".join([str(z) for z in numbers]))
        logger.debug(decoded)
        decoded_values.append(decoded)
        
    if PART_1:
        return unique_output_counts

    return sum(decoded_values)


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.debug("Logger init")
    year = 2021
    day = 8

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

    if args.print_data:
        for line in lines:
            print(line)

        sys.exit(0)

    ##################### Solution

    print("Solution:", solve(lines=lines))
    print("done.")

# end

