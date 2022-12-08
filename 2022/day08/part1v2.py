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
