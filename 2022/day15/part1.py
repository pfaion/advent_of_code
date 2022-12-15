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
