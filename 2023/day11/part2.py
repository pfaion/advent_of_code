from itertools import combinations
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

galaxies = [
    (x, y)
    for x, line in enumerate(data_raw)
    for y, cell in enumerate(line)
    if cell == "#"
]

empty_rows = {i for i, row in enumerate(data_raw) if "#" not in row}
empty_cols = {i for i, col in enumerate(zip(*data_raw)) if "#" not in col}

path_sum = 0
for a, b in combinations(galaxies, 2):
    a_x, b_x = sorted((a[0], b[0]))
    a_y, b_y = sorted((a[1], b[1]))
    distance = 0
    for x in range(a_x, b_x):
        distance += 1000000 if x in empty_rows else 1
    for y in range(a_y, b_y):
        distance += 1000000 if y in empty_cols else 1
    path_sum += distance

print(path_sum)
