"""
    problem_2021_22.py
"""

import queue
import re
import sys

import logging
from flood_advent.utils import init_logging
from flood_advent.utils import LOGGER_NAME
from flood_advent.utils import parse_args
from flood_advent.utils import Input

logger = logging.getLogger(LOGGER_NAME)

PART_1 = False


def cubes_intersect(cube_1, cube_2):
    x_overlaps = cube_1.x1 <= cube_2.x2 and cube_1.x2 >= cube_2.x1
    y_overlaps = cube_1.y1 <= cube_2.y2 and cube_1.y2 >= cube_2.y1
    z_overlaps = cube_1.z1 <= cube_2.z2 and cube_1.z2 >= cube_2.z1
    return x_overlaps and y_overlaps and z_overlaps


class Cube:
    def __init__(self, x1, x2, y1, y2, z1, z2, onoff):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
        self.onoff = onoff

    def split_x(self, x1, x2):
        cube_1 = Cube(self.x1, x1, self.y1, self.y2, self.z1, self.z2, self.onoff)
        cube_2 = Cube(x2, self.x2, self.y1, self.y2, self.z1, self.z2, self.onoff)
        return [cube_1, cube_2]

    def split_y(self, y1, y2):
        cube_1 = Cube(self.x1, self.x2, self.y1, y1, self.z1, self.z2, self.onoff)
        cube_2 = Cube(self.x1, self.x2, y2, self.y2, self.z1, self.z2, self.onoff)
        return [cube_1, cube_2]

    def split_z(self, z1, z2):
        cube_1 = Cube(self.x1, self.x2, self.y1, self.y2, self.z1, z1, self.onoff)
        cube_2 = Cube(self.x1, self.x2, self.y1, self.y2, z2, self.z2, self.onoff)
        return [cube_1, cube_2]

    def volume(self):
        return (
            (self.x2 + 1 - self.x1) * (self.y2 + 1 - self.y1) * (self.z2 + 1 - self.z1)
        )

    def num_on_points(self):
        if self.onoff == "on":
            return self.volume()
        return 0

    def __repr__(self):
        return f"Cube: ({self.x1},{self.x2},{self.y1},{self.y2},{self.z1},{self.z2}) '{self.onoff}' vol. {self.volume()}"


class Core:
    def __init__(self):
        self.cubes = {}

    def __repr__(self):

        ret = "------Universe------\n"
        ret += "\n".join([str(c) for c in self.cubes])
        return ret

    def replace_cube(self, old, new_list):
        """
        The old cube has been split into two new cubes.
        Discard the old one and add the new ones
        """
        # logger.debug("replacing %s with %s", old, new_list)
        del self.cubes[old]
        for x in new_list:
            self.cubes[x] = 1

    def num_on_points(self):
        """
        Return the total number of points
        in the Core that are turned on
        """
        total = 0
        for c in self.cubes.keys():
            total += c.num_on_points()

        return total

    def process_new_cube(self, new_cube):
        logger.debug("Adding new cube: %s", new_cube)

        # add all current cubes to queue
        #
        process_queue = queue.Queue()
        for k in self.cubes.keys():
            process_queue.put(k)

        while not process_queue.empty():
            e_cube = process_queue.get()
            # logger.debug("Examining current cube %s", e_cube)

            if not cubes_intersect(new_cube, e_cube):
                # logger.debug("%s and %s do not overlap", new_cube, e_cube)
                pass

            elif e_cube.x1 < new_cube.x1:
                new_cubes = e_cube.split_x(new_cube.x1 - 1, new_cube.x1)
                self.replace_cube(e_cube, new_cubes)
                for c in new_cubes:
                    process_queue.put(c)
            elif e_cube.x2 > new_cube.x2:
                new_cubes = e_cube.split_x(new_cube.x2, new_cube.x2 + 1)
                self.replace_cube(e_cube, new_cubes)
                for c in new_cubes:
                    process_queue.put(c)

            elif e_cube.y1 < new_cube.y1:
                new_cubes = e_cube.split_y(new_cube.y1 - 1, new_cube.y1)
                self.replace_cube(e_cube, new_cubes)
                for c in new_cubes:
                    process_queue.put(c)
            elif e_cube.y2 > new_cube.y2:
                new_cubes = e_cube.split_y(new_cube.y2, new_cube.y2 + 1)
                self.replace_cube(e_cube, new_cubes)
                for c in new_cubes:
                    process_queue.put(c)

            elif e_cube.z1 < new_cube.z1:
                new_cubes = e_cube.split_z(new_cube.z1 - 1, new_cube.z1)
                self.replace_cube(e_cube, new_cubes)
                for c in new_cubes:
                    process_queue.put(c)
            elif e_cube.z2 > new_cube.z2:
                new_cubes = e_cube.split_z(new_cube.z2, new_cube.z2 + 1)
                self.replace_cube(e_cube, new_cubes)
                for c in new_cubes:
                    process_queue.put(c)

            else:
                # The new cube completely encompasses the existing cube
                # so discard the existing cube
                del self.cubes[e_cube]

        # if the new cube is "on", add it to the core.
        # otherwise, silently discard it
        if new_cube.onoff == "on":
            self.cubes[new_cube] = 1

    def add_cube(self, x1, x2, y1, y2, z1, z2, onoff):

        # Part 1 ignores cubes outside of -50, 50 in each dimension
        if PART_1 == True:
            if x1 > 50 or y1 > 50 or z1 > 50:
                return
            if x2 < -50 or y2 < -50 or z2 < -50:
                return

        new_cube = Cube(x1, x2, y1, y2, z1, z2, onoff)
        self.process_new_cube(new_cube)


def solve(lines):
    """
    on x=10..12,y=10..12,z=10..12
    on x=11..13,y=11..13,z=11..13
    off x=9..11,y=9..11,z=9..11
    on x=10..10,y=10..10,z=10..10
    """
    sc = Core()

    for line in lines:

        if line.startswith("#"):
            # logger.warning("skipping commented line %s", line)
            continue

        # logger.debug("processing input line: %s", line)
        m = re.match(
            r"(o[^ ]+) x=([-0-9]+)..([-0-9]+),y=([-0-9]+)..([-0-9]+),z=([-0-9]+)..([-0-9]+)",
            line,
        )

        info = {
            "onoff": m.group(1),
            "x1": int(m.group(2)),
            "x2": int(m.group(3)),
            "y1": int(m.group(4)),
            "y2": int(m.group(5)),
            "z1": int(m.group(6)),
            "z2": int(m.group(7)),
        }
        sc.add_cube(
            info["x1"],
            info["x2"],
            info["y1"],
            info["y2"],
            info["z1"],
            info["z2"],
            info["onoff"],
        )

    print(sc)
    return sc.num_on_points()


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    init_logging(is_verbose=args.verbose)
    logger = logging.getLogger(LOGGER_NAME)

    logger.debug("Logger init")
    year = 2021
    day = 22

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
