
from flood_advent.utils import get_integers_from_file


# This is the same input
INPUT_FILE="data/2018/day/1/input.txt"

line_generator = get_integers_from_file(filepath=INPUT_FILE)



#line_generator = [1, -1]
#line_generator = [3, 3, 4, -2, -4]


input_lines = list(line_generator)

value = 0
f = {0: 1}
while True:
    #print(value)
    print("Iterating")
    for line in input_lines:
        #print(f"adding {line}")
        value += line
        #print(f"new frequency: {value}")
        f.setdefault(value, 0)
        f[value] += 1
        #print(f)

        if f[value] >= 2:
            print(f"first repeated frequency: {value}")
            raise Exception()
            




