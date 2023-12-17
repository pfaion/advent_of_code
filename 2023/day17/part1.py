from collections import defaultdict
from pathlib import Path
from queue import PriorityQueue

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()
inf = float("inf")
heat_losses = defaultdict(lambda: inf)
for row, line in enumerate(data_raw):
    for col, cell in enumerate(line):
        heat_losses[(row, col)] = int(cell)


def get_next(path: list[tuple[int, int]]) -> set[tuple[int, int]]:
    assert len(path) > 0
    row, col = path[-1]
    if len(path) == 1:
        return {(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)}

    result = set()
    n_same_row = sum(r == row for r, _ in path[-4:-1]) + 1
    if n_same_row <= 3:
        dcol = col - path[-2][1]
        if dcol >= 0:
            result.add((row, col + 1))
        if dcol <= 0:
            result.add((row, col - 1))
    n_same_col = sum(c == col for _, c in path[-4:-1]) + 1
    if n_same_col <= 3:
        drow = row - path[-2][0]
        if drow >= 0:
            result.add((row + 1, col))
        if drow <= 0:
            result.add((row - 1, col))
    return result


LEFT = 1
UP = 2
RIGHT = 3
DOWN = 4


def get_direction_and_count(path: list[tuple[int, int]]) -> tuple[int, int]:
    assert len(path) > 1
    row, col = path[-1]
    n_same_row = sum(r == row for r, _ in path[-4:-1]) + 1
    n_same_col = sum(c == col for _, c in path[-4:-1]) + 1
    if path[-1][0] > path[-2][0]:
        return DOWN, n_same_col
    if path[-1][0] < path[-2][0]:
        return UP, n_same_col
    if path[-1][1] > path[-2][1]:
        return RIGHT, n_same_row
    if path[-1][1] < path[-2][1]:
        return LEFT, n_same_row


start = (0, 0)
target = (len(data_raw) - 1, len(data_raw[0]) - 1)

distances = {}
q = PriorityQueue()
q.put((0, [start]))
while not q.empty():
    loss, path = q.get()

    if path[-1] == target:
        print(loss)
        break

    for n in get_next(path):
        expanded = path + [n]
        new_loss = loss + heat_losses[n]
        direction, count = get_direction_and_count(expanded)

        if new_loss < distances.get((n, direction, count), inf):
            distances[(n, direction, count)] = new_loss
            q.put((new_loss, expanded))
