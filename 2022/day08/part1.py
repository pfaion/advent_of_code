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
