import re
from itertools import pairwise
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

edge = {(0, 0)}
minrow, maxrow, mincol, maxcol = 0, 0, 0, 0

row, col = (0, 0)
for line in data_raw:
    direction, str_count = re.match(r"([UDLR]) (\d+)", line).groups()
    count = int(str_count)
    for _ in range(count):
        if direction == "U":
            row -= 1
            minrow = min(minrow, row)
        elif direction == "D":
            row += 1
            maxrow = max(maxrow, row)
        elif direction == "L":
            col -= 1
            mincol = min(mincol, col)
        elif direction == "R":
            col += 1
            maxcol = max(maxcol, col)
        edge.add((row, col))

area = 0
inside = False
for row in range(minrow, maxrow + 1):
    down, up = False, False
    print(f"{row:<4}", end="")
    for col in range(mincol, maxcol + 1):
        if (row, col) in edge:
            if (row - 1, col) in edge:
                up = True
            if (row + 1, col) in edge:
                down = True
            if up and down:
                inside = not inside
            area += 1
            print("#", end="")
        else:
            up = down = False
            if inside:
                area += 1
                print("#", end="")
            else:
                print(".", end="")
    print()

print(area)
