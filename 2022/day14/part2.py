from itertools import pairwise
from math import copysign
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()

# parse cave
cave = {}
start = (500, 0)
minx, maxx, miny, maxy = (start[0], start[0], start[1], start[1])
for line in data:
    points = [list(map(int, point.split(","))) for point in line.split(" -> ")]
    for p in points:
        minx = min(minx, p[0])
        maxx = max(maxx, p[0])
        miny = min(miny, p[1])
        maxy = max(maxy, p[1])
    for p1, p2 in pairwise(points):
        while p1 != p2:
            cave[tuple(p1)] = "R"
            if p1[0] != p2[0]:
                p1[0] += copysign(1, p2[0] - p1[0])
            if p1[1] != p2[1]:
                p1[1] += copysign(1, p2[1] - p1[1])
        cave[tuple(p1)] = "R"
minx, maxx, miny, maxy = map(int, (minx, maxx, miny, maxy))
floor = maxy + 2

# pour sand
sand = start
while True:
    if sand[1] < floor and (
        (new := (sand[0], sand[1] + 1)) not in cave
        or (new := (sand[0] - 1, sand[1] + 1)) not in cave
        or (new := (sand[0] + 1, sand[1] + 1)) not in cave
    ):
        sand = new
    else:
        cave[sand] = "S"
        if start in cave:
            break
        sand = start

# for y in range(miny, maxy + 1):
#     for x in range(minx, maxx + 1):
#         print(cave.get((x, y), " ").replace("R", "█").replace("S", "░"), end="")
#     print()

print(sum(1 for v in cave.values() if v == "S"))
