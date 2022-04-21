"""
    2021 Day 19 part 2
"""
import itertools
import pprint

data = """

0 (0, 0, 0) face: 0 rotation: 0
2 (108, -1254, -76) face: 2 rotation: 0
8 (-1155, -1259, -2) face: 1 rotation: 1
10 (101, -1192, -1169) face: 5 rotation: 1
12 (41, -1150, 1244) face: 5 rotation: 2
15 (-1007, -1211, 1138) face: 5 rotation: 3
18 (94, -1150, -2517) face: 3 rotation: 1
19 (84, -1142, 2403) face: 2 rotation: 2
24 (-2255, -1123, -11) face: 1 rotation: 2
25 (1222, -1292, 1106) face: 2 rotation: 2
26 (42, -84, 1161) face: 4 rotation: 1
4 (59, 1202, 1119) face: 2 rotation: 1
5 (1248, -92, 1150) face: 1 rotation: 3
6 (1226, 1228, 1133) face: 0 rotation: 3
7 (1337, -2482, 1108) face: 0 rotation: 1
13 (1380, -1177, 2341) face: 3 rotation: 0
14 (147, -2303, -2414) face: 4 rotation: 3
16 (2528, -2466, 1184) face: 4 rotation: 0
17 (63, -2422, 2442) face: 5 rotation: 0
21 (3650, -2428, 1199) face: 1 rotation: 0
22 (2512, -32, 1212) face: 3 rotation: 3
23 (1386, 1215, 23) face: 0 rotation: 2
1 (1359, -2363, 2386) face: 4 rotation: 1
3 (1219, 2450, 1192) face: 1 rotation: 2
9 (3788, -1230, 1220) face: 4 rotation: 2
11 (1274, 2314, -144) face: 3 rotation: 2
20 (1316, 3662, 1082) face: 2 rotation: 3

"""


lines = data.split("\n")
points = []
for line in lines:
    data = line.strip()
    if data:
        coords = "".join(data.split(' ')[1:4])
        coords = coords.strip('(')
        coords = coords.strip(')')
        coords = coords.split(',')
        coords = [int(a) for a in coords]
        points.append(coords)
#pprint.pprint(points)

combos = list(itertools.permutations(points, 2))
#pprint.pprint(combos)


def mandist(p1, p2):
    x = abs(p1[0] - p2[0])
    y = abs(p1[1] - p2[1])
    z = abs(p1[2] - p2[2])
    tot = x + y + z
    return tot

max_man = 0
for com in combos:
    d = mandist(*com)
    if d > max_man:
        max_man = d

print(max_man)
