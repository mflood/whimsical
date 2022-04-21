from typing import List
from enum import IntEnum

from itertools import combinations

from flood_advent.utils import get_integers_from_file
from flood_advent.utils import get_input_from_file


# This is the same input
INPUT_FILE="data/2018/day/2/input.txt"

line_generator = get_input_from_file(filepath=INPUT_FILE)


#line_generator = [1, -1]
#line_generator = [3, 3, 4, -2, -4]


class MatchType(IntEnum):
    kTwo = 2
    kThree = 3


def match_types(string: str) -> List[MatchType]:
    ret = []
    d = {}
    twos = {}
    threes = {}
    box_ids = []
    for letter in string:
        d.setdefault(letter, 0)
        d[letter] += 1

        if d[letter] == 2:
            twos[letter] = True
        elif d[letter] == 3:
            threes[letter] = True
            del twos[letter]
        elif d[letter] == 4:
            del threes[letter]

        if len(ret) == 2:
            break

    has_2 = 0
    has_3 = 0
    if twos:
        has_2 = 1
    if threes:
        has_3 = 1

    return [has_2, has_3]


ret = match_types(string = "ababab")


input_lines = list(line_generator)

totals = [0, 0]
box_ids = []
for line in input_lines:

    has_2, has_3 = match_types(string=line)
    if has_2 or has_3:
        box_ids.append(line)
        
    totals[0] += has_2
    totals[1] += has_3


print("Part 1: checksum")
print(totals)
print(totals[0] * totals[1])

        
def common_letters(string1, string2):
    common = ""
    for idx, letter in enumerate(string1):
        if string2[idx] == letter:
            common += letter

    return common



combos = combinations(box_ids, r=2)
for combo in combos:
    str1, str2 = combo[0], combo[1]
    common = common_letters(str1, str2)
    if len(common) == len(str1) -1:
        print(common)
        break


