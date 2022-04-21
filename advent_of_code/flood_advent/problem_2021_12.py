"""
    problem_2021_12.py
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

PART_1 = 1



class Node():

    def __init__(self, name):
        self.name = name
        self.small = True
        if self.name < "Z":
            self.small = False
        logger.info("%s small= %s", self.name, self.small)
        self.target_nodes = []
        self.visited = []

    def add_link(self, other_node):
        if other_node not in self.target_nodes:
            self.target_nodes.append(other_node)

    def get_target_names(self):

        for t in self.target_nodes:
            yield t.name

    def __str__(self):
        target_names = ", ".join(list(self.get_target_names()))
        return f"{self.name} --> {target_names}"

    def get_traversals(self, current_path):
        
        names = [n.name for n in current_path]
        logger.debug("getting traversals for %s -> %s", names, self.name)

        if self.name == "start" and self.name in names:
            logger.debug("ignoring start again")
            return []

        if self.small:
            small_names = [n.name for n in current_path if n.small]
            visited_twice = [n for n in small_names if small_names.count(n)> 1]
            
            if visited_twice and self.name in small_names:
                return []
                logger.debug("Small cave %s already exists in current_path and visited twice already happend (%s)", self.name, visited_twice[0])
            
        new_path = copy.copy(current_path)
        new_path.append(self)

        if self.name == "end":
            logger.debug("end")
            return [new_path]

        return_traversals = []
        for t in self.target_nodes:
            return_traversals.extend(t.get_traversals(new_path))
        return return_traversals
     

class CaveSystem():

    def __init__(self):
        self.node_dict = {}

    def get_traversals(self):
        traversals = self.node_dict["start"].get_traversals(current_path=[])
        as_strings = []
        for t in traversals:
            s = ",".join([n.name for n in t])
            if s not in as_strings:
                as_strings.append(s)
        as_strings.sort()
        return as_strings

     
    def link(self, a, b):
        logger.info("Connecting %s - %s", a, b)
        na = self.node_dict.get(a, Node(name=a))
        self.node_dict[a] = na
        nb = self.node_dict.get(b, Node(name=b))
        self.node_dict[b] = nb

        if a != "end" and b != "start":
            na.add_link(nb)

        if b != "end" and a != "start":
            nb.add_link(na)

    def print(self):
        for k, v in self.node_dict.items():
            logger.info("%s: %s", k, v)
        
def solve(lines):

    start_node = None
    cs = CaveSystem()
    for line in lines:
        a, b = line.split('-')
        cs.link(a, b)

    cs.print()
    traversals = cs.get_traversals()
    for idx, t in enumerate(traversals):
        logger.info("traversal %s: %s", idx + 1, t)
    return len(traversals)


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.info("Logger init for %s", sys.argv[0])
    year = 2021
    day = 12

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

