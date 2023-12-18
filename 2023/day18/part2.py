import re
from collections import defaultdict
from itertools import batched, combinations
from pathlib import Path

from rich import print

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

vertices_per_row = defaultdict(list)

row, col = (0, 0)
for line in data_raw:
    hex_count, dir_str = re.search(r"#([0-9a-f]{5})([0-9a-f])", line).groups()
    direction = "RDLU"[int(dir_str)]
    count = int(hex_count, 16)
    if direction == "U":
        row -= count
    elif direction == "D":
        row += count
    elif direction == "L":
        col -= count
    elif direction == "R":
        col += count
    vertices_per_row[row].append(col)

vertices_per_row = {row: sorted(cols) for row, cols in vertices_per_row.items()}

area = 0
type Range = tuple[int, int]
current_ranges: list[Range] = []
prev_row = 0
for row in sorted(vertices_per_row.keys()):
    cols = vertices_per_row[row]
    row_ranges = [(a, b) for a, b in batched(cols, 2)]

    # add rectangle area between vertex rows
    width = sum(b - a + 1 for (a, b) in current_ranges)
    height = row - prev_row - 1
    prev_row = row
    area += width * height

    # add vertex row
    vertex_row = list(current_ranges) + list(row_ranges)
    while True:
        N = len(vertex_row)
        for i, j in combinations(range(N), 2):
            (a1, a2) = vertex_row[i]
            (b1, b2) = vertex_row[j]
            if not (a2 < b1 or b2 < a1):
                # they intersect
                merged = (min(a1, b1), max(a2, b2))
                vertex_row.pop(j)
                vertex_row.pop(i)
                vertex_row.append(merged)
                break
        else:
            break
    area += sum(b - a + 1 for (a, b) in vertex_row)

    # compute new range
    while row_ranges:
        (r1, r2) = row_ranges.pop()
        inside = []
        extends = []
        for c1, c2 in current_ranges:
            if c1 <= r1 <= r2 <= c2:
                inside.append((c1, c2))
            if r2 == c1 or c2 == r1:
                extends.append((c1, c2))
        assert len(inside) <= 1
        assert len(extends) <= 2
        assert not (inside and extends)
        if inside:
            c1, c2 = inside[0]
            current_ranges.remove((c1, c2))
            if c1 == r1 and c2 == r2:
                pass
            elif c1 == r1:
                current_ranges.append((r2, c2))
            elif c2 == r2:
                current_ranges.append((c1, r1))
            else:
                current_ranges.extend(((c1, r1), (r2, c2)))
        elif extends:
            for c1, c2 in extends:
                current_ranges.remove((c1, c2))
                r1 = min(r1, c1)
                r2 = max(r2, c2)
            current_ranges.append((r1, r2))
        else:
            current_ranges.append((r1, r2))
        assert not any(a == b for a, b in current_ranges)

print(area)
