from math import prod
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()

n_rows = len(data)
n_cols = len(data[0])

# 1D data makes slicing easier
data1d = "".join(data)


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
