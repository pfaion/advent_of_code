# Day 17

[Exercise Text](https://adventofcode.com/2023/day/17)

## Part 1
```python
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

```
Runtime: 2.385s, Size: 2183, Output:
```
967
```
## Part 2
### Overview
| Variant | Runtime | Size |
| --- | --- | --- |
|1|8.907s|2905|
|2|2.036s|2142|

### Variant 1
```python
from collections import defaultdict
from itertools import takewhile
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
    drow = row - path[-2][0]
    dcol = col - path[-2][1]
    n_same_row = len(list(takewhile(lambda x: x[0] == row, reversed(path))))
    n_same_col = len(list(takewhile(lambda x: x[1] == col, reversed(path))))

    if drow != 0:
        if n_same_col <= 10:
            if drow > 0:
                result.add((row + 1, col))
            else:
                result.add((row - 1, col))
        if n_same_col >= 5:
            result.add((row, col + 1))
            result.add((row, col - 1))

    if dcol != 0:
        if n_same_row <= 10:
            if dcol > 0:
                result.add((row, col + 1))
            else:
                result.add((row, col - 1))
        if n_same_row >= 5:
            result.add((row + 1, col))
            result.add((row - 1, col))

    return result


def get_direction_and_count(path: list[tuple[int, int]]) -> tuple[int, int]:
    assert len(path) > 1
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4

    row, col = path[-1]
    n_same_row = len(list(takewhile(lambda x: x[0] == row, reversed(path))))
    n_same_col = len(list(takewhile(lambda x: x[1] == col, reversed(path))))
    if path[-1][0] > path[-2][0]:
        return DOWN, n_same_col
    if path[-1][0] < path[-2][0]:
        return UP, n_same_col
    if path[-1][1] > path[-2][1]:
        return RIGHT, n_same_row
    if path[-1][1] < path[-2][1]:
        return LEFT, n_same_row


def can_stop(path: list[tuple[int, int]]) -> bool:
    assert len(path) > 0
    row, col = path[-1]
    n_same_row = len(list(takewhile(lambda x: x[0] == row, reversed(path))))
    n_same_col = len(list(takewhile(lambda x: x[1] == col, reversed(path))))
    return n_same_row >= 5 or n_same_col >= 5


start = (0, 0)
target = (len(data_raw) - 1, len(data_raw[0]) - 1)

distances = defaultdict(lambda: inf)
q = PriorityQueue()
q.put((0, [start]))
while not q.empty():
    loss, path = q.get()

    if path[-1] == target and can_stop(path):
        print(loss)
        break

    for n in get_next(path):
        expanded = path + [n]
        new_loss = loss + heat_losses[n]

        direction, count = get_direction_and_count(expanded)
        key = (n, direction, count)

        if new_loss < distances[key]:
            distances[key] = new_loss
            q.put((new_loss, expanded))

```
Runtime: 8.907s, Size: 2905, Output:
```
1101
```
### Variant 2
```python
from collections.abc import Iterator
from enum import IntEnum
from pathlib import Path
from queue import PriorityQueue

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()
heat_losses = {
    (row, col): int(cell)
    for row, line in enumerate(data_raw)
    for col, cell in enumerate(line)
}
inf = float("inf")


class Direction(IntEnum):
    NONE = 0
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4


type Point = tuple[int, int]
type Cost = int


def walk(p: Point, d: Direction) -> Point:
    row, col = p
    if d == Direction.UP:
        return (row, col - 1)
    elif d == Direction.DOWN:
        return (row, col + 1)
    if d == Direction.LEFT:
        return (row - 1, col)
    elif d == Direction.RIGHT:
        return (row + 1, col)


def get_next(
    p: Point, how_we_got_there: Direction
) -> Iterator[tuple[Point, Cost, Direction]]:
    D = Direction
    new_directions = {
        D.NONE: (D.UP, D.DOWN, D.LEFT, D.RIGHT),
        D.LEFT: (D.UP, D.DOWN),
        D.RIGHT: (D.UP, D.DOWN),
        D.UP: (D.LEFT, D.RIGHT),
        D.DOWN: (D.LEFT, D.RIGHT),
    }
    current_paths_and_costs = {d: ([p], 0) for d in D}
    for distance in range(1, 11):
        for d in new_directions[how_we_got_there]:
            path, cost = current_paths_and_costs[d]
            new_p = walk(path[-1], d)
            additional_cost = heat_losses.get(new_p, inf)
            new_cost = cost + additional_cost
            current_paths_and_costs[d] = (path + [new_p], new_cost)
            if distance >= 4 and new_cost != inf:
                yield (new_p, new_cost, d)


start = (0, 0)
target = (len(data_raw) - 1, len(data_raw[0]) - 1)

costs = {}
q = PriorityQueue()
q.put((0, (0, 0), Direction.NONE))
while not q.empty():
    cost, p, how_we_got_there = q.get()

    if p == target:
        print(cost)
        break

    for n, additional_cost, outgoing_direction in get_next(p, how_we_got_there):
        new_cost = cost + additional_cost
        key = (n, outgoing_direction)
        if new_cost < costs.get(key, inf):
            costs[key] = new_cost
            q.put((new_cost, n, outgoing_direction))

```
Runtime: 2.036s, Size: 2142, Output:
```
1101
```