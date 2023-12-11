from itertools import combinations
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

expanded_rows = []
for row in data_raw:
    expanded_rows.append(row)
    if "#" not in row:
        expanded_rows.append(row)

expanded_full = []
transposed = list(zip(*expanded_rows))
for column in transposed:
    expanded_full.append(column)
    if "#" not in column:
        expanded_full.append(column)


galaxies = [
    (x, y)
    for x, line in enumerate(expanded_full)
    for y, cell in enumerate(line)
    if cell == "#"
]


print(
    sum(
        path_length := abs(a_x - b_x) + abs(a_y - b_y)
        for (a_x, a_y), (b_x, b_y) in combinations(galaxies, 2)
    )
)
