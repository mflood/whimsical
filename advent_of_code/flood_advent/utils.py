
import argparse
import re
import logging
import requests
from typing import Iterator
from typing import List

LOGGER_NAME="advent"

def init_logging(is_verbose: bool):
    """
        Creates standard logging for the logger_name passed in
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    channel = logging.StreamHandler()
    if is_verbose:
        channel.setLevel(logging.DEBUG)
    else:
        channel.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(filename)s:%(lineno)s: %(message)s')
    channel.setFormatter(formatter)
    logger.addHandler(channel)
    logger.debug("Initialized logging")

    return logger


def get_input_from_file(filepath: str) -> Iterator[str]:
    """
        Read the file from the internet and return 
        an iterator of each line as a string
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.info("Reading input from %s", filepath)
    with open(filepath, "r") as handle:
        for line in handle:
            line = line.strip()
            yield line

def read_comma_separated_values(filepath: str) -> Iterator[str]:
    logger = logging.getLogger(LOGGER_NAME)
    logger.info("Reading comma separated values from %s", filepath)
    return_list = []
    for line in get_input_from_file(filepath=filepath):
        line = line.strip()
        values = line.split(",")
        for value in values:
            v = value.strip()
            if v:
                yield v

def read_comma_separated_ints(filepath: str) -> Iterator[int]:
    values = read_comma_separated_values(filepath=filepath)
    for item in values:
        yield int(item)


def get_integers_from_file(filepath: str) -> Iterator[int]:
    """
        Read the file from the internet and return 
        an iterator of each line as a string
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.info("Reading integers from %s", filepath)
    for line in get_input_from_file(filepath=filepath):
        yield int(line)


def line_to_parts(line) -> dict:
    """
        #123 @ 3,2: 5x4
        ID: #123
        from_left: 3
        from_top: 2
        width: 5
        height: 4
    """
    m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
    
    m = re.match(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line)
    return_dict = {
        "id": m.group(1),
        "from_left": m.group(2),
        "from_top": m.group(3),
        "width": m.group(4),
        "height": m.group(5),
    }
    return return_dict 


def binary_list_to_int(binary_list: List[str]) -> int:
    """
        convert 
           ["1", "0", "1"]
        or [1, 0, 1]
        to 5
    """
    # convert to strings
    binary_list = [str(x) for x in binary_list]

    as_string = "".join(binary_list)
    as_int= int(as_string, 2)
    return as_int



class SparseGrid():

    def __init__(self):
        self.cell_dict = {}
        self.max_x = 0
        self.max_y = 0
        self._logger = logging.getLogger(LOGGER_NAME)

    def add_line(self, x1, y1, x2, y2, value, only_horizontal):

        # only horizontal and vertical lines
        if not (x1 == x2 or y1 == y2) and only_horizontal:
            self._logger.debug("Not a horizontal or vertical line")
            return

        min_x = min(x1, x2)
        max_x = max(x1, x2)
        min_y = min(y1, y2)
        max_y = max(y1, y2)

        # Adjust sparse grid metadata for printing the grid
        if max_x > self.max_x:
            self.max_x = max_x
            self._logger.debug("Adjusting sparse grid max_x to %s", self.max_x)

        if max_y > self.max_y:
            self.max_y = max_y
            self._logger.debug("Adjusting sparse grid max_y to %s", self.max_y)


        # use range to get coordinates
        x_list = list(range(min_x, max_x + 1))
        y_list = list(range(min_y, max_y + 1))

        # reverse the range if needed
        if x1 < x2:
            x_list.reverse()

        if y1 < y2:
            y_list.reverse()

        # for vertical lines, duplicate the x value
        # for each coordinate so zip works
        if len(y_list) == 1:
            for x in range(len(x_list)-1):
                y_list.append(y_list[0])

        # for horizontal lines, duplicate the y value
        # for each coordinate so zip works
        if len(x_list) == 1:
            for y in range(len(y_list)-1):
                x_list.append(x_list[0])

        cells = list(zip(x_list, y_list))
        for x, y in cells:
            coordinate = f"{x}:{y}"
            self.cell_dict.setdefault(coordinate, [])
            self.cell_dict[coordinate].append(value)

    def add_block(self, from_left_x: int, from_top_y: int, width: int, height: int, value: str):

        if from_left_x + width > self.max_x:
            self.max_x = from_left_x + width
            print(f"Adjusting width to {self.max_x}")
        if from_top_y + height > self.max_y:
            self.max_y = from_top_y + height
            print(f"Adjusting height to {self.max_y}")

        for x in range(width):
            for y in range(height):
                true_x = x + from_left_x
                true_y = y + from_top_y
                coordinate = f"{true_x}:{true_y}"
                self.cell_dict.setdefault(coordinate, [])
                self.cell_dict[coordinate].append(value)


    def evaluate_block(self, from_left_x: int, from_top_y: int, width: int, height: int, value: str) -> bool:
        """
            One the SparseGrid is populated, evaluate a block to
            see if it does not overlap with any other block
        """
        for x in range(width):
            for y in range(height):
                true_x = x + from_left_x
                true_y = y + from_top_y
                coordinate = f"{true_x}:{true_y}"
                array = self.cell_dict[coordinate]
                if len(array) != 1:
                    return False

        return True
        

    def get_num_overlapping_cells(self):
        """
            return the number of cells with arrays
            with more than one element
        """
        num = 0
        for coord, array in self.cell_dict.items():
            if len(array) > 1:
                num += 1
        return num


    def print(self):
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                coordinate = f"{x}:{y}"
                array = self.cell_dict.get(coordinate)
                if not array:
                    print(".", end='')
                else:
                    print(len(array), end='')

            print("")
                


def parse_args(argv=None):
    """
        Parse command line args
    """
    parser = argparse.ArgumentParser(description="Main Driver for Frivenmeld")

    parser.add_argument('-v',
                        action="store_true",
                        dest="verbose",
                        required=False,
                        help="Debug output")

    parser.add_argument('-t',
                        action="store_true",
                        dest="use_test_data",
                        required=False,
                        help="Use test data")

    parser.add_argument('-d',
                        action="store_true",
                        dest="print_data",
                        required=False,
                        help="Just print out the data")

    parser.add_argument('--part',
                        dest="part",
                        choices=[1, 2],
                        type=int,
                        default=1,
                        required=False,
                        help="Solve part 1 or 2")

    parser.add_argument("-yd",
                        dest="year_day",
                        help="YYYYDD the date to process data for")

    results = parser.parse_args(argv)
    return results 



class Input():

    def __init__(self, year: int, day: int, use_test_data: bool):
        self._year = year
        self._day = day
        self._use_test_data = use_test_data
        self._logger = logging.getLogger(LOGGER_NAME)
        self._logger.info("Input year: %d day: %d test-data: %s", self._year, self._day, self._use_test_data) 

    def get_filepath(self):
        if self._use_test_data: 
            return f"data/{self._year}/day/{self._day}/test-input.txt"
        else:
            return f"data/{self._year}/day/{self._day}/input.txt"
    
    def get_raw(self) -> str:
        filepath = self.get_filepath()
        self._logger.info("Reading raw data from '%s'", filepath)
        with open(filepath, "r") as handle:
            data = handle.read()
            return data

    def get_lines(self) -> Iterator[str]:
        filepath = self.get_filepath()
        self._logger.info("Reading lines from '%s'", filepath)
        with open(filepath, "r") as handle:
            for line in handle:
                line = line.strip()
                yield line

    def get_chars(self) -> List[str]:
        """
            return all the characters in the file as a list
            asd
            fro
            ['a', 's', 'd', 'f', 'r', 'o']
        """
        for line in self.get_lines():
            for char in line:
                yield char

    def get_ints(self) -> Iterator[int]:
        for line in self.get_lines():
            yield int(line)
        
    def get_floats(self) -> Iterator[int]:
        for line in self.get_lines():
            yield float(line)
        
    def get_comma_separated_values(self) -> Iterator[str]:
        """
            note: skips empty values
        """
        for line in self.get_lines():
            line = line.strip()
            values = line.split(",")
            for value in values:
                v = value.strip()
                if v:
                    yield v

    def get_comma_separated_ints(self) -> Iterator[int]:
        values = self.get_comma_separated_values()
        for item in values:
            yield int(item)



