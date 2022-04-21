"""
    problem_2021_23.py
"""

import queue
import re
import sys
import copy
from typing import List, Any, Generator, Iterator
from dataclasses import dataclass
from enum import IntEnum

import itertools
import logging
from flood_advent.utils import line_to_parts
from flood_advent.utils import SparseGrid
from flood_advent.utils import init_logging
from flood_advent.utils import LOGGER_NAME
from flood_advent.utils import binary_list_to_int
from flood_advent.utils import parse_args
from flood_advent.utils import Input

logger = logging.getLogger(LOGGER_NAME)

PART_1 = False


class Creature():
   
    def __init__(self, creature_type, movement_cost, loc_x, loc_y):
        self.movement_cost = movement_cost
        self.creature_type = creature_type
        self.loc_x = loc_x
        self.loc_y = loc_y
 
class Room():

    def __init__(self, x, creature_type, occ1, occ2):
        self.x
        self.create_type = create_type
        self.spaces = [None, None]

class BurrowMapnn():

    def __init__(self):
        self.hall = []

    def load_from_raw(self, lines):
        self.map = []
        for line in lines:
            array = [l for l in line]
            self.map.append(array)

    def print(self):
        for row_set in self.map:
            for space in row_set:
                print(space, end="")
            print("")


    def get_moves(self):
        """
            Return possible map states
        """
        

    def get_state_hash(self):
        """
            Return a hashable state
        """
        return tuple([tuple([x for x in row if x not in [' ', '#']]) for row in self.map[1:-1]])


class BurrowState():
    """
        ('.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'),
        ('A', 'D', 'A', 'B'), 
        ('C', 'C', 'D', 'B'))
    """

    def __init__(self, map_state):
        self.hallway = [x for x in map_state[0]]
        self.rooms = list(zip(map_state[1], map_state[2]))
        self.score = None
        self.prev_node = None
        self.visited = None

    def get_map_state(self):
        return tuple([tuple(self.hallway), 
                      tuple([x[0] for x in self.rooms]),
                      tuple([x[1] for x in self.rooms]))

    def __lt__(self, other):
        """
            For priority queue
        """
        return self.score < other.score

    def move_from_room_to_hallway(self, room_type, x):
        target_rooms = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        room_index = target_rooms[room_type]
        room = self.rooms[room_index]
        if room[0] in ['A', 'B', 'C', 'D']:
            monster_type = room[0]
            room[0] = '.'
        else:
            monster_type = room[1]
            room[1] = '.'

        logger.info("Moving room %s monster %s to hallway %s", room_type, monster_type, x)
        self.hallway[x] = monster_type

    def cost_from_room_to_point(self, monster_type, x):
        logger.info("Finding cost from room %s to hallway %s", x, monster_type)

        room_index = target_rooms[monster_type]
        room = self.rooms[room_index]
        other_monster = None
        if room[0] in ['A', 'B', 'C', 'D']:
            moving_monster = room[0]
            other_monster = room[1]
            if other_monster == monster_type and moving_monster == monster_type:
                logger.error("Room %s already has both monsters in it")
                return None
        elif room[1] in ['A', 'B', 'C', 'D']:
            moving_monster = room[1]
            if moving_monster == monster_type:
                logger.error("Monster %s is already in place in room %s", moving_monster, monster_type)
                return None
        else:
            logger.error("No monsters in room %s to move", monster_type)
            return None

        move_costs = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
        target_rooms = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        target_rooms = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        target_room_x = {'A': 2, 'B': 4, 'C': 6, 'D': 8}

        move_cost = move_costs[monster_type]
        room_x = target_room_x[monster_type]

        if room_x < x:
            x_steps = [x for x in range(room_x, x)]
        else:
            x_steps = [x for x in range(x + 1, room_x + 1)]
        logger.info("hallway steps are %s", x_steps)


    def cost_from_point_to_room(self, x, monster_type):
        logger.info("Finding cost from hallway %s to room %s", x, monster_type)
        move_costs = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
        target_rooms = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        target_rooms = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        target_room_x = {'A': 2, 'B': 4, 'C': 6, 'D': 8}

        move_cost = move_costs[monster_type]
        room_index = target_rooms[monster_type]
        room = self.rooms[room_index]
        room_x = room_x[monster_type]

        if room_x < x:
            x_steps = [x for x in range(room_x, x)]
        else:
            x_steps = [x for x in range(x + 1, room_x + 1)]
        logger.info("hallway steps are %s", x_steps)

        total_cost = 0
        for x in x_steps:
            if self.hallway[x] != '.':
                # blocked!
                logger.error("Path is blocked by %s", self.hallway[x])
                return None
            total_cost += move_cost

        if room[0] != '.':
            # room has no openings
            logger.error("Room %s does not have space!", monster_type)
            return None

        total_cost += move_cost
        
        if room[1] == '.':
            # last spot is empty
            total_cost += move_cost
        elif room[1] != monster_type:
            # we can't move here yet!!
            logger.error("Can't move into room %s because of %s", monster_type, room[1])
            return None

        return total_cost
        

    def get_possible_next_states(self):

        for room_type in ['A', 'B', 'C', 'D']:
            for x in range(11):
                cost = self.cost_from_room_to_point(monster_type=room_type, x=x)
                if cost is not None:

                    
                    

        for idx, item in enumerate(self.hallway):
            if item:
                move_cost[item]
                target_room = target_rooms[item]
                room_x = target_room_x[item]
                if idx < room_x:
                    for x in range(idx+1, room_x + 1):

                        pass


class PathFinder():

    def __init__(self, bs: BurrowState):

        bs.score = 0
        node_hash = bs.get_state_hash()
        state_map = { node_hash: bs}

    def get_possible_next_states(burrow):


        return burrowState(
            
        )

    def find_shortest_path(start_map_state, end_map_state):
        

        bs = BurrowState(start_map_state)
        bs.score = 0
        current_node = bs
        next_queue = queue.PriorityQueue()

        while current_node:
            if current_node == end_map_state:
                logger.info("Found END!")
                return
            if current_node.visited:
                current_node = next_queue.get()
                continue
            
            neighbors = current_node.get_possible_next_states()



class T:
    def __lt__(self, other):
        """
            For priority queue
        """
        return self.score < other.score

    def __str__(self):
        return str(self.display)

    def __repr__(self):
        return f"({self.x}, {self.y})[{self.risk}]"


def solve(lines):

    start_state = (
        ('.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'),
        ('A', 'D', 'A', 'B'), 
        ('C', 'C', 'D', 'B'))

    end_state = (
        ('.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'),
        ('A', 'B', 'C', 'D'), 
        ('A', 'B', 'C', 'D'))

    burrow_state = BurrowState(start_state) 

    test_state = (
        ('.', '.', '.', 'A', '.', '.', '.', '.', '.', '.', '.'),
                  ('.',      '.',      'C',      '.'), 
                  ('A',      'C',      'D',      '.'))

    burrow_state = BurrowState(test_state) 
    print(burrow_state.cost_from_point_to_room(0, 'A'))
    print(burrow_state.cost_from_point_to_room(0, 'B'))
    print(burrow_state.cost_from_point_to_room(0, 'C'))
    print(burrow_state.cost_from_point_to_room(0, 'D'))
    print(burrow_state.cost_from_point_to_room(3, 'A'))
    print(burrow_state.cost_from_point_to_room(3, 'B'))
    print(burrow_state.cost_from_point_to_room(3, 'C'))
    print(burrow_state.cost_from_point_to_room(3, 'D'))
    print(burrow_state.cost_from_point_to_room(10, 'A'))
    print(burrow_state.cost_from_point_to_room(10, 'B'))
    print(burrow_state.cost_from_point_to_room(10, 'C'))
    print(burrow_state.cost_from_point_to_room(10, 'D'))



    # burrow_map = BurrowMap()
    # burrow_map.load_from_raw(lines=adjusted_lines)



if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.debug("Logger init")
    year = 2021
    day = 23

    if args.year_day:
        year = int(args.year_day[:4])
        day = int(args.year_day[4:])

    problem_input = Input(year=year, day=day, use_test_data=args.use_test_data)
    lines = problem_input.get_lines()
    # lines  = problem_input.get_floats()
    # lines  = problem_input.get_ints()

    # convert from generator to list
    lines = list(lines)
    logger.info("Loaded %d values", len(lines))

    if args.print_data:
        for line in lines:
            print(line)

        sys.exit(0)

    ##################### Solution
    print("Solution:", solve(lines=lines))
    print("done.")

# end
