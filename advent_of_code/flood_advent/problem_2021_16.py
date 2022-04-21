"""
    problem_2021_16.py
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

def hex_to_bin(data):
    map = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
    } 
    ret = ''
    for letter in data:
        ret += map[letter]
                
    return ret

    #scale = 16 ## hexadecimal
    #num_of_bits = 4
    #as_bin = bin(int(data, scale))[2:].zfill(num_of_bits)
    #if len(as_bin) % 4:
    #    missing_zeros = 4 - (len(as_bin) % 4)
    #    as_bin = "0" * missing_zeros + as_bin
    #return as_bin

def bin_to_int(value):
    """
        0101 -> 5
    """
    logger.debug("Converting binary '%s' to int", value)
    as_int = int(value, 2)
    logger.debug("bin: '%s' = int: '%s'", value, as_int)
    return as_int


def pull_bits(size, data) -> (str, str):
    """
        11110000, 3 -> (111, 10000)
    """
    logger.debug("pulling %s bits from %s bits", size, len(data))
    left = data[:size]
    right = data[size:]
    left_display = left
    right_display = right
    if len(left_display) > 30:
        left_display = f"{left[:30]}..."
    if len(right_display) > 30:
        right_display = f"{right[:30]}..."
    logger.debug("pulled '%s' (%s bytes) / '%s' (%s bytes)", left_display, len(left), right_display, len(right))
    return left, right


def version_type_data(binary_string) -> (int, int, str):
    """
        return the version, type and trailing data
    """
    version_b, binary_string = pull_bits(3, binary_string)
    version_int = bin_to_int(version_b)

    type_b, binary_string = pull_bits(3, binary_string)
    type_int = bin_to_int(type_b)
    
    return version_int, type_int, binary_string


def parse_literal(data) -> (int, str):
    """
        parses literal and returns remaining data
    """
    logger.debug("Parsing literal: %s", data)        
    parts = []
    remaining = data
    while True:
        group, remaining = pull_bits(5, remaining)
        keep_going = int(group[0])
        val = group[1:]
        logger.debug("group: %s (%s:%s)", group, keep_going, val)
        parts.append(val)
        if not keep_going:
            break

    logger.debug("got parts: %s", parts)
    full_bin = "".join(parts)
    as_int = bin_to_int(full_bin)
    logger.debug("As int: %s", as_int)
    return as_int, remaining


def test():
    assert(bin_to_int("0000") == 0)
    assert(bin_to_int("0001") == 1)
    assert(bin_to_int("0101") == 5)
    assert(bin_to_int("1111") == 15)
    assert(bin_to_int("1010") == 10)
    assert pull_bits(3, "101000111") == ("101", "000111")
    assert pull_bits(0, "101000111") == ("", "101000111")
    val, remaining = parse_literal("10000100001000000101AAAAA")
    assert(val == 5)
    assert(remaining == "AAAAA")


class Packet():
    pass

class Operator(Packet):

    def __init__(self, version, t):
        self.version = version
        self.ptype = t
        self.values = []

    @property
    def value(self):
        if self.ptype == 0: # sum
            values = [x.value for x in self.values]
            return sum(values)

        elif self.ptype == 1: # product
            total = 1
            for x in self.values:
                total *= x.value
            return total

        elif self.ptype == 2: # min
            values = [x.value for x in self.values]
            return min(values)

        elif self.ptype == 3: # max
            values = [x.value for x in self.values]
            return max(values)

        elif self.ptype == 5: # >
            if self.values[0].value > self.values[1].value:
                return 1
            else:
                return 0

        elif self.ptype == 6: # <
            if self.values[0].value < self.values[1].value:
                return 1
            else:
                return 0

        elif self.ptype == 7: # ==
            if self.values[0].value == self.values[1].value:
                return 1
            else:
                return 0

    def version_sum(self):
        total = self.version
        for x in self.values:
            total += x.version_sum()
        return total

    def __repr__(self):
        #join_string = f" <{self.ptype}v{self.version}> "
        #return f"({self.ptype}v{self.version}: " + join_string.join([str(x) for x in self.values]) + ")"
        if self.ptype == 0:
            return "( " + " + ".join([str(x) for x in self.values]) + " )"
        if self.ptype == 1:
            return "( " + " * ".join([str(x) for x in self.values]) + " )"
        if self.ptype == 2:
            return "min( " + ", ".join([str(x) for x in self.values]) + " )"
        if self.ptype == 3:
            return "max( " + ", ".join([str(x) for x in self.values]) + " )"
        if self.ptype == 5:
            return "gt( " + ", ".join([str(x) for x in self.values]) + " )"
        if self.ptype == 6:
            return "lt( " + ", ".join([str(x) for x in self.values]) + " )"
        if self.ptype == 7:
            return "eq( " + ", ".join([str(x) for x in self.values]) + " )"

class Literal(Packet):

    def __init__(self, version, ptype, value):
        self.version = version
        self.ptype = ptype
        self.value = value

    def version_sum(self):
        return self.version

    def __repr__(self):
        return f"{self.value}"
        #return f"lit.v{self.version}={self.value}"


def create_packet(data) -> (Packet, str):

    v, t, data = version_type_data(data)
    if t == 4:
        value, data = parse_literal(data)
        packet = Literal(v, t, value)
        return packet, data
    else:
        logger.debug("--------------- Parsing operator-----------")
        operator = Operator(v, t)
        mode, data = pull_bits(1, data)
        mode = int(mode)        
        if mode == 0:
            logger.debug("Using mode 0. finding total_length")
            s_length, data = pull_bits(15, data)
            length = bin_to_int(s_length)
            logger.debug("total length of subpackets: %s", length)
            next_subpacket_data, remaining = pull_bits(length, data)
            logger.debug("pulled %s bytes for subpacket(s). %s bytes remainin.", len(next_subpacket_data), len(remaining))
            sub_packets = []
            first = True
            while first or next_subpacket_data:
                first = False
                logger.debug("Recursive call to creating child packet with data length %s", len(next_subpacket_data))
                sub_packet, next_subpacket_data = create_packet(next_subpacket_data)
                logger.debug("Recursive call returned with operator %s and %s bytes of remaining data", sub_packet, len(next_subpacket_data))
                operator.values.append(sub_packet)

        elif mode == 1:
            logger.debug("Using mode 1, finding num subpackets")
            s_num, remaining = pull_bits(11, data)
            num_sub_packets = bin_to_int(s_num)
            logger.debug("num_sub_packets: %s", num_sub_packets)
            for x in range(num_sub_packets):
                logger.debug("Creating child packet #%s", x + 1)
                packet, remaining = create_packet(remaining)
                operator.values.append(packet)
        else:
            raise Exception("Invalid mode: %s" % mode)

        logger.debug("returning operator and %s bytes of data: %s", len(remaining), operator)
        return operator, remaining
        

def solve(lines):

    data = lines[0]
    logger.debug(data)
    as_bin = hex_to_bin(data)
    logger.debug(as_bin)
    p, leftover_data = create_packet(data=as_bin)
    logger.info("Final Packet: %s", p)
    logger.info("version sum: %s", p.version_sum())
    logger.info("final value: %s", p.value)
    return 0


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.info("Logger init for %s", sys.argv[0])
    year = 2021
    day = 16

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

    test()
    print("Solution:", solve(lines=lines))
    print("done.")

# end

