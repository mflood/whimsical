"""
    problem_2021_15.py
"""

import sys
from typing import List, Any, Generator, Iterator 
from dataclasses import dataclass
import pprint
from enum import IntEnum
import queue

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

PART_1 = 1

class Node():
    def __init__(self, x, y, risk):
        self.x = x
        self.y = y
        self.risk = risk
        self.display = risk
        self.score = None
        self.prev_node = None
        self.visited = None

    def __lt__(self, other):
        """
            For priority queue
        """
        return self.score < other.score

    def __str__(self):
        return str(self.display)

    def __repr__(self):
        return f"({self.x}, {self.y})[{self.risk}]"

class RiskMap():

    def __init__(self, lines):
        self.lines = lines
        self.width = len(lines[0])
        self.height = len(lines)
        logger.info("new map: %s x %s", self.width, self.height)
        self.nodes = []
        for y in range(self.height):
            new_row = []
            self.nodes.append(new_row)
            for x in range(self.width):
                value = int(self.lines[y][x])
                node = Node(x, y, value)
                new_row.append(node)

    def find_shortest_path(self, start_x, start_y, end_x, end_y):

        start_node = self.nodes[start_y][start_x]
        end_node = self.nodes[end_y][end_x]

        start_node.score = 0
        current_node = start_node
        next_queue = queue.PriorityQueue()

        while current_node: 
            if current_node == end_node:
                logger.info("Found END node!!")
                return
            if current_node.visited:
                current_node = next_queue.get()
                continue

            neighbors = self.get_all_neighbors(current_node.x, current_node.y)
            neighbors = [n for n in neighbors if not n.visited]

            for n in neighbors:
                score = n.risk + current_node.score
                if n.score is None or n.score > score:
                    n.score = score
                    n.prev_node = current_node
                next_queue.put(n)

            current_node.visited = 1
            current_node = next_queue.get()

    
    def score(self, x, y):
        return self.nodes[y][x].score

    def highlight_path_to(self, x, y):
        current_node = self.nodes[y][x]
        while current_node:
            #logger.info("highlighting %s", current_node)
            current_node.display = '*'
            current_node = current_node.prev_node

    def get_all_neighbors(self, source_x, source_y):
        logger.debug("getting neighbors for (%s, %s)", source_x, source_y)
        return_list = []
        for y in [-1, 1]:
            true_y = source_y + y
            if true_y >= self.height or true_y < 0:
                continue
            node = self.nodes[true_y][source_x]
            return_list.append(node)

        for x in [-1, 1]:
            true_x = source_x + x
            if true_x >= self.width or true_x < 0:
                continue
            node = self.nodes[source_y][true_x]
            return_list.append(node)
        logger.debug(return_list)
        return return_list

    def print(self):
        for y in range(self.height):
            for x in range(min(self.width, 250)):
                print(self.nodes[y][x].__str__(), end="")

            print("")


def expand_lines(lines):
    # make the map 5 times bigger along x and y
    # based on rules

    new_lines = []
    for row in lines:
        new_row = []
        for x in range(5):
            for i in range(len(lines[0])):
                value = int(row[i]) + x
                if value > 9:
                    value = value % 9
                new_row.append(value)

        new_lines.append("".join([str(x) for x in new_row]))


    more_lines = []
    for level in range(5):
        for row in new_lines:
            adj = [int(x) + level for x in row]
            adj = list(map(lambda x: x % 9 if x > 9 else x, adj))
            more_lines.append("".join([str(x) for x in adj]))

    return more_lines


def solve(lines):

    lines = expand_lines(lines)
    # return 0
    riskMap = RiskMap(lines=lines)
    #riskMap.print()
    riskMap.find_shortest_path(0, 0, riskMap.width-1, riskMap.height-1) 
    riskMap.highlight_path_to(riskMap.width-1, riskMap.height-1)
    riskMap.print()
    return riskMap.score(riskMap.width-1, riskMap.height-1)



if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.info("Logger init for %s", sys.argv[0])
    year = 2021
    day = 15

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

    # -d just show the data
    if args.print_data:
        for line in lines:
            print(line)
        sys.exit(0)

    print("Solution:", solve(lines=lines))
    print("done.")

# end

