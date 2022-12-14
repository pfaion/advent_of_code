# Day 14

[Exercise Text](https://adventofcode.com/2022/day/14)

## Part 1
```python
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

# pour sand
sand = start
while True:
    if sand[1] > maxy:
        break
    elif (new := (sand[0], sand[1] + 1)) not in cave:
        sand = new
    elif (new := (sand[0] - 1, sand[1] + 1)) not in cave:
        sand = new
    elif (new := (sand[0] + 1, sand[1] + 1)) not in cave:
        sand = new
    else:
        cave[sand] = "S"
        sand = start

# for y in range(miny, maxy + 1):
#     for x in range(minx, maxx + 1):
#         print(cave.get((x, y), " ").replace("R", "█").replace("S", "░"), end="")
#     print()

print(sum(1 for v in cave.values() if v == "S"))

```
Runtime: 0.095s, Size: 1431, Output:
```
1078
```
## Part 2
### Overview
| Variant | Runtime | Size |
| --- | --- | --- |
|1|1.795s|1453|
|2|0.095s|1783|

### Variant 1
```python
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

```
Runtime: 1.795s, Size: 1453, Output:
```
30486
```
### Variant 2
```python
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
# idea: don't trickle every grain from top, but re-use previous trickle path
trickle_path = [start]
while trickle_path:
    # go back up the trickle path until the last one that hasn't set yet
    while trickle_path and (end := trickle_path[-1]) in cave:
        trickle_path.pop()
    # continue trickling from there
    while trickle_path:
        if end[1] < floor and (
            (new := (end[0], end[1] + 1)) not in cave
            or (new := (end[0] - 1, end[1] + 1)) not in cave
            or (new := (end[0] + 1, end[1] + 1)) not in cave
        ):
            trickle_path.append(new)
            end = new
        else:
            cave[end] = "S"
            break

# for y in range(miny, maxy + 1):
#     for x in range(minx, maxx + 1):
#         print(cave.get((x, y), " ").replace("R", "█").replace("S", "░"), end="")
#     print()

print(sum(1 for v in cave.values() if v == "S"))

```
Runtime: 0.095s, Size: 1783, Output:
```
30486
```