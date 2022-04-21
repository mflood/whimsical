
from flood_advent.utils import get_integers_from_file


INPUT_FILE="data/2018/day/1/input.txt"

line_generator = get_integers_from_file(filepath=INPUT_FILE)
print(line_generator)

value = 0
for line in line_generator:
    print(line)
    value += line

print(f"Final value: {value}")







