# Day 11

[Exercise Text](https://adventofcode.com/2023/day/11)

## Part 1
```python
from itertools import combinations
from pathlib import Path

from rich import print

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

```
Runtime: 0.076s, Size: 739, Output:
```
9639160
```
## Part 2
```python
from itertools import combinations
from pathlib import Path

from rich import print

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

```
Runtime: 0.769s, Size: 776, Output:
```
752936133304
```