# Day 15

[Exercise Text](https://adventofcode.com/2022/day/15)

## Part 1
```python
import re
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()

target_row = 2000000
ranges = []
for line in data:
    sx, sy, bx, by = map(int, re.findall(r"[xy]=(-?\d+)", line))
    beacon_dist = abs(sx - bx) + abs(sy - by)
    target_row_dist = abs(sy - target_row)
    target_row_radius = beacon_dist - target_row_dist
    if target_row_radius <= 0:
        continue
    _range = (sx - target_row_radius, sx + target_row_radius)
    non_overlaps = []
    overlaps = [_range]
    for r in ranges:
        if r[0] <= _range[0] <= r[1] or r[0] <= _range[1] <= r[1]:
            overlaps.append(r)
        else:
            non_overlaps.append(r)
    lower_bounds, upper_bounds = zip(*overlaps)
    merged = (min(lower_bounds), max(upper_bounds))
    ranges = non_overlaps + [merged]

print(sum(abs(r[1] - r[0]) for r in ranges))

```
Runtime: 0.032s, Size: 873, Output:
```
5832528
```
## Part 2
```python
import re
import sys
from pathlib import Path
from typing import Iterator

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()
data = [list(map(int, re.findall(r"[xy]=(-?\d+)", line))) for line in data_raw]
bound_min, bound_max = 0, 4000000

Point = tuple[int, int]
SensorArea = tuple[int, Point]  # radius, center


def get_outline(area: SensorArea) -> Iterator[Point]:
    radius, center = area
    r = radius + 1
    x, y = center[0], center[1]
    yield (x, y - r)
    yield (x, y + r)
    for i in range(1, r):
        offset = r - i
        yield (x + i, y + offset)
        yield (x + i, y - offset)
        yield (x - i, y + offset)
        yield (x - i, y - offset)
    yield (x - r, y)
    yield (x + r, y)


def dist(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def check_bounds(p: Point) -> bool:
    return bound_min <= p[0] <= bound_max and bound_min <= p[1] <= bound_max


# sort areas by radius, so when we iterate over their outlines, we start with
# the small ones
areas: list[SensorArea] = sorted(
    ((abs(sx - bx) + abs(sy - by), (sx, sy)) for sx, sy, bx, by in data)
)

for i, area in enumerate(areas):

    # sort other areas by distance to this area, increases chance that find an
    # overlap faster
    other_areas = sorted(
        areas[:i] + areas[i + 1 :], key=lambda other: dist(other[1], area[1])
    )

    # check each sensor outline if it lies within the bounding box and if it's
    # covered by at least one other sensor
    for p in get_outline(area):
        if not check_bounds(p):
            continue

        for radius, center in other_areas:
            if dist(p, center) <= radius:
                break
        else:
            # this point does not lie in any other sensor area
            print(p[0] * 4000000 + p[1])
            sys.exit()

```
Runtime: 2.53s, Size: 1848, Output:
```
13360899249595
```