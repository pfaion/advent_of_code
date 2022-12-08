# Day 8

[Exercise Text](https://adventofcode.com/2022/day/8)

## Part 1
### Overview
| Variant | Runtime | Size |
| --- | --- | --- |
|1|0.038s|1278|
|2|0.066s|769|

### Variant 1
```python
from itertools import accumulate
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()

visible_coordinates: set[tuple[int, int]] = set()

for row_idx, row in enumerate(data):
    left_hull = list(accumulate(row, max))
    left_visible_col_idxs = [left_hull.index(height) for height in set(left_hull)]
    for col_idx in left_visible_col_idxs:
        visible_coordinates.add((row_idx, col_idx))

    right_hull = list(accumulate(reversed(row), max))
    right_visible_col_idxs = [right_hull.index(height) for height in set(right_hull)]
    for col_idx in right_visible_col_idxs:
        visible_coordinates.add((row_idx, len(row) - 1 - col_idx))

transposed_data = list(zip(*data))

for col_idx, col in enumerate(transposed_data):
    top_hull = list(accumulate(col, max))
    top_visible_row_idxs = [top_hull.index(height) for height in set(top_hull)]
    for row_idx in top_visible_row_idxs:
        visible_coordinates.add((row_idx, col_idx))

    bottom_hull = list(accumulate(reversed(col), max))
    bottom_visible_row_idxs = [bottom_hull.index(height) for height in set(bottom_hull)]
    for row_idx in bottom_visible_row_idxs:
        visible_coordinates.add((len(col) - 1 - row_idx, col_idx))

print(len(visible_coordinates))

```
Runtime: 0.038s, Size: 1278, Output:
```
1546
```
### Variant 2
```python
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()

# 1D data makes slicing easier
data1d = "".join(data)
n_cols = len(data[0])


def idx_to_rowcol(idx: int) -> tuple[int, int]:
    return (idx // n_cols, idx % n_cols)


n_visible = 0

# iterate over all trees
for idx, height in enumerate(data1d):
    row_idx, col_idx = idx_to_rowcol(idx)

    # slice out treelines to the edges
    left = data1d[idx - col_idx : idx]
    right = data1d[idx + 1 : (row_idx + 1) * n_cols]
    top = data1d[col_idx:idx:n_cols]
    bottom = data1d[idx + n_cols :: n_cols]

    for direction in (left, right, top, bottom):
        if all(others < height for others in direction):
            n_visible += 1
            break

print(n_visible)

```
Runtime: 0.066s, Size: 769, Output:
```
1546
```
## Part 2
```python
from math import prod
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()

# 1D data makes slicing easier
data1d = "".join(data)
n_cols = len(data[0])


def idx_to_rowcol(idx: int) -> tuple[int, int]:
    return (idx // n_cols, idx % n_cols)


max_scenic_score = 0

# iterate over all trees
for idx, height in enumerate(data1d):
    row_idx, col_idx = idx_to_rowcol(idx)

    # slice out treelines to the edges
    left = data1d[idx - col_idx : idx][::-1]
    right = data1d[idx + 1 : (row_idx + 1) * n_cols]
    top = data1d[col_idx:idx:n_cols][::-1]
    bottom = data1d[idx + n_cols :: n_cols]

    def count_visible_trees(treeline: str) -> int:
        # find first index that's of greater or equal height, index plus one
        # gives the number of trees
        return next(
            (i + 1 for i, h in enumerate(treeline) if h >= height),
            len(treeline),  # default if all are smaller
        )

    scenic_score = prod(map(count_visible_trees, (left, right, top, bottom)))
    max_scenic_score = max(max_scenic_score, scenic_score)

print(max_scenic_score)

```
Runtime: 0.079s, Size: 1124, Output:
```
519064
```