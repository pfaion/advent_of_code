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

    # we want to check other areas for overlap with the outline. we can
    # pre-filter this list to only consider those that overlap at all
    other_areas = [
        other
        for other in areas[:i] + areas[i + 1 :]
        if dist(other[1], area[1]) <= other[0] + area[0]
    ]

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
