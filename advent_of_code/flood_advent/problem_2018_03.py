from typing import List
from enum import IntEnum

from itertools import combinations

from flood_advent.utils import get_integers_from_file
from flood_advent.utils import get_input_from_file
from flood_advent.utils import line_to_parts
from flood_advent.utils import SparseGrid


# This is the same input
INPUT_FILE="data/2018/day/3/input.txt"
line_generator = get_input_from_file(filepath=INPUT_FILE)

#line_generator = [1, -1]
#line_generator = [3, 3, 4, -2, -4]


test_lines = [
"#1 @ 1,3: 4x4",
"#2 @ 3,1: 4x4",
"#3 @ 5,5: 2x2"]

lines = list(line_generator)

grid = SparseGrid()
for line in lines:
    as_parts = line_to_parts(line)
    # {'id': '3', 'from_left': '5', 'from_top': '5', 'width': '2', 'height': '2'}
    grid.add_block(
        from_left_x=int(as_parts['from_left']),
        from_top_y=int(as_parts['from_top']),
        width=int(as_parts['width']),
        height=int(as_parts['height']),
        value=as_parts['id'])

    #grid.print()


num_overlaps = grid.get_num_overlapping_cells()
print(num_overlaps)

# find single non-overlapping block
for line in lines:
    as_parts = line_to_parts(line)
    is_alone = grid.evaluate_block(
        from_left_x=int(as_parts['from_left']),
        from_top_y=int(as_parts['from_top']),
        width=int(as_parts['width']),
        height=int(as_parts['height']),
        value=as_parts['id'])

    if is_alone:
        print(as_parts['id'])
        break


