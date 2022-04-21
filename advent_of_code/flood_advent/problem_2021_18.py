"""
    problem_2021_18.py
"""

import itertools
import math
import json
import re
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


class SplitMe(Exception):
    pass


class ExplodeException(Exception):
    pass

class SplitException(Exception):
    pass


class Literal():

    def __init__(self, value):
        self.value = value
        
    def magnitude(self):
        return self.value

    def explode(self, level):
        return 

    def split(self):
        if self.value >= 10:
            logger.debug("Split me!!! %s", self)
            raise SplitMe()

    def depth(self, level):
        return level

    def max_value(self):
        return self.value

    def add_to_first_left_literal(self, value):
        self.value += value

    def add_to_first_right_literal(self, value):
        self.value += value

    def __repr__(self):
        return f"{self.value}"
        #return f"*{self.value}*"


class Node():

    def __init__(self, left, right, parent):
        self.parent = parent
        self.left = left
        self.right = right
        if isinstance(left, int):
            self.left = Literal(left)
        elif isinstance(left, Node):
            self.left = left
            left.parent = self
        else:
            self.left = Node(*left, self)

        if isinstance(right, int):
            self.right = Literal(right)
        elif isinstance(right, Node):
            self.right = right
            right.parent = self
        else:
            self.right = Node(*right, self)

    def first_right_not_me(self, me):
        if self.right != me:
            return self.right
        if self.parent:
            return self.parent.first_right_not_me(self)
        return None

    def first_left_not_me(self, me):
        if self.left != me:
            return self.left
        if self.parent:
            return self.parent.first_left_not_me(self)
        return None

    def add_to_first_left_literal(self, value):
        self.left.add_to_first_left_literal(value)

    def add_to_first_right_literal(self, value):
        self.right.add_to_first_right_literal(value)

    def max_value(self):
        return max(self.left.max_value(), self.right.max_value())

    def depth(self, level=0):
        level += 1
        ret = max(self.left.depth(level), self.right.depth(level))
        return ret

    def replace_child_with_literal(self, child, literal):
        if self.left == child:
            self.left = literal
        elif self.right == child:
            self.right = literal
        else:
            raise Exception()

    def split(self):
        
        try:
            self.left.split()
        except SplitMe:
            logger.debug("Splitting %s", self.left)
            left_value = math.floor(self.left.value / 2 )
            right_value = math.ceil(self.left.value / 2)
            self.left = Node(left_value, right_value, self)
            raise SplitException()

        try:
            self.right.split()
        except SplitMe:
            logger.debug("Splitting %s", self.right)
            left_value = math.floor(self.right.value / 2 )
            right_value = math.ceil(self.right.value / 2)
            self.right = Node(left_value, right_value, self)
            raise SplitException()

    def explode(self, level=0):

        logger.debug("Reducing %s, level %s", self, level)
        if level == 4:
            logger.debug("Explode this pair: %s", self)
            left_node = self.parent.first_left_not_me(self)
            if left_node:
                left_node.add_to_first_right_literal(self.left.value)

            right_node = self.parent.first_right_not_me(self)
            if right_node:
                right_node.add_to_first_left_literal(self.right.value)
           
            self.parent.replace_child_with_literal(self, Literal(0))
            raise ExplodeException()
        else:
            self.left.explode(level = level + 1)
            self.right.explode(level = level + 1)

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()


    def __repr__(self):
        #return f"<{self.left}, {self.right}>"
        return f"[{self.left}, {self.right}]"
    

def line_to_node(line):

    as_json = json.loads(line)
    node = Node(*as_json, None)
    return node


def reduce_node(node):
    logger.debug("Reducing node: %s", node)
    while True:
        logger.debug("Depth: %s", node.depth())
        if node.depth() >= 5:
            logger.debug("Attempting Explode")
            try:
                node.explode()
                raise Exception("Should have exploded!")
            except ExplodeException:
                logger.debug(node)

        elif node.max_value() >= 10:
            logger.debug("max value greater than 10: %s", node)
            try:
                logger.debug("Forcing split")
                node.split()
            except SplitException:
                pass
        else:
            return node


def solve_b(lines):

    p = list(itertools.permutations(lines, 2))
    max_set = None
    max_mag = None
    max_node = None
    for (a, b) in p:
        a_node = reduce_node(line_to_node(a))
        b_node = reduce_node(line_to_node(b))
        node = Node(a_node, b_node, None)
        node = reduce_node(node)
        magnitude = node.magnitude()

        if not max_node or magnitude > max_mag:
            max_mag = magnitude
            max_set = (a, b)
            max_node = node
            
    logger.info("Max magnitude: %s", max_mag)

def solve(lines):

    is_first = True
    current_node = None
    for line in lines:
        new_node = line_to_node(line)
        new_node = reduce_node(new_node)
        if is_first:
            is_first = False
            current_node = new_node
        else:
            
            current_node = Node(current_node, new_node, None)
            current_node = reduce_node(current_node)
        logger.info(current_node)

        logger.info("Processed: %s", current_node)
        logger.info("Magnitude: %s", current_node.magnitude())
        

if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.info("Logger init for %s", sys.argv[0])
    year = 2021
    day = 18

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

    print("Solution:", solve_b(lines=lines))
    print("done.")

# end

