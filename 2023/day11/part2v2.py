from itertools import pairwise
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

galaxies = [
    (row, col)
    for row, row_data in enumerate(data_raw)
    for col, cell in enumerate(row_data)
    if cell == "#"
]
N = len(galaxies)

spacing = 1000000
result = 0
for dimension in map(sorted, zip(*galaxies)):
    for i, (g1, g2) in enumerate(pairwise(dimension), 1):
        distance = 0 if g1 == g2 else (g2 - g1 - 1) * spacing + 1
        factor = i * (N - i)
        result += distance * factor

print(result)
