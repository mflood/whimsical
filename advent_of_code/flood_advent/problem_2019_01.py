from typing import List, Any, Generator, Iterator 
from enum import IntEnum

from itertools import combinations

from flood_advent.utils import get_integers_from_file
from flood_advent.utils import get_input_from_file
from flood_advent.utils import line_to_parts
from flood_advent.utils import SparseGrid

YEAR=2019
DAY=1

def get_test_lines() -> List[Any]:
    test_lines = [
    12,
    14,
    1969,
    100756,
    ]
    return test_lines
    

def get_file_lines() -> List[Any]:

    # This is the same input
    INPUT_FILE=f"data/{YEAR}/day/{DAY}/input.txt"
    line_generator = get_integers_from_file(filepath=INPUT_FILE)
    #line_generator = get_input_from_file(filepath=INPUT_FILE)
    return line_generator


def get_lines(use_test_data: bool) -> List[Any]:
    if use_test_data:
        return get_test_lines()
    return get_file_lines()

####### Solution ###########

def calc_fuel(mass: int):

    div_3 = int(mass / 3)
    sub_2 = div_3 - 2
    if sub_2 <= 0:
        return 0
    return sub_2 + calc_fuel(mass=sub_2)


lines = list(get_lines(use_test_data=False))
my_sum = 0
for item in lines:
    my_sum += calc_fuel(mass=item) 


print(my_sum)

# end
