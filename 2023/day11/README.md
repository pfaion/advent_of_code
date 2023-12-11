# Day 11

[Exercise Text](https://adventofcode.com/2023/day/11)

## Part 1
```python
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

```
Runtime: 0.038s, Size: 715, Output:
```
9639160
```
## Part 2
### Overview
| Variant | Runtime | Size |
| --- | --- | --- |
|1|0.733s|752|
|2|0.023s|565|

### Variant 1
```python
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

```
Runtime: 0.733s, Size: 752, Output:
```
752936133304
```
### Variant 2
```python
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

```
Runtime: 0.023s, Size: 565, Output:
```
752936133304
```