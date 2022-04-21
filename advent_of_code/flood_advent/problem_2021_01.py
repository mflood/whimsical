"""
    Advent of code 2021 day 1
"""
from typing import List
from flood_advent.utils import get_integers_from_file

INPUT_FILE = "data/2021/day/1/input.txt"
line_generator = get_integers_from_file(filepath=INPUT_FILE)

test_lines = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263,
]

lines = list(line_generator)
# lines = list(test_lines)


# part 1: increasing values
#


def find_increases(value_list: List[int]) -> int:
    """
    Count the number of times an item in
    the list has a greater value than the
    item it follows.
    """
    last = None
    count = 0
    for line in value_list:

        if not last:
            last = line
            continue

        if line > last:
            count += 1
        last = line

    return count


print("part 1: %s" % find_increases(value_list=lines))


# part 2
# sliding windows
#


def accumulate_sliding_windows(value_list: List[int], window_size: int) -> List[int]:

    windows = []

    # e.g [[], [None], [None, None]]
    for x in range(window_size):
        windows.append([None] * x)

    window_values = []
    for value in value_list:

        for idx, window in enumerate(windows):

            # initial delay of each window
            if None in window:
                window.pop()
                continue

            window.append(value)

            # When a window accumulates the right number
            # of items (e.g. 3), sum the values and
            # append that to the return list.
            # Then reset the window to empty.
            if len(window) == window_size:
                window_values.append(sum(window))
                windows[idx] = []

    return window_values


window_values = accumulate_sliding_windows(value_list=lines, window_size=3)
print("part 2: %s" % find_increases(value_list=window_values))

# end
