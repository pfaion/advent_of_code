import re
from itertools import pairwise
from pathlib import Path

from rich import print

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

vertices = []
minrow = 0

row, col = (0, 0)
for line in data_raw:
    direction, str_count = re.match(r"([UDLR]) (\d+)", line).groups()
    count = int(str_count)
    if direction == "U":
        row -= count
        minrow = min(minrow, row)
    elif direction == "D":
        row += count
    elif direction == "L":
        col -= count
    elif direction == "R":
        col += count
    vertices.append((row, col))

topleft = min((v for v in vertices if v[0] == minrow), key=lambda v: v[1])


def get_direction(a, b) -> str:
    row, col = a
    nrow, ncol = b
    if nrow > row:
        return "D"
    elif nrow < row:
        return "U"
    elif ncol > col:
        return "R"
    elif ncol < col:
        return "L"
    assert False


outer_vertices = []
(row, col) = topleft
i = vertices.index((row, col))
N = len(vertices)
next_dir = get_direction((row, col), vertices[(i + 1) % N])
assert next_dir in "DR"
clockwise_factor = -1 if next_dir == "D" else 1
prev_dir = "U"
for offset in range(1, len(vertices) + 1):
    next_i = N + i + clockwise_factor * offset
    next_v = vertices[next_i % len(vertices)]
    next_dir = get_direction((row, col), next_v)
    match prev_dir + next_dir:
        case "UL" | "LL" | "LU":
            outer_vertices.append((row + 1, col))
        case "UU" | "UR" | "RU" | "RR":
            outer_vertices.append((row, col))
        case "RD" | "DR" | "DD":
            outer_vertices.append((row, col + 1))
        case "DL" | "LD":
            outer_vertices.append((row + 1, col + 1))

    row, col = next_v
    prev_dir = next_dir

# shoelace formula (https://en.wikipedia.org/wiki/Polygon#Simple_polygons)
print(
    int(
        0.5
        * abs(sum(xa * yb - xb * ya for (xa, ya), (xb, yb) in pairwise(outer_vertices)))
    )
)
# Incorrect already on part 1
