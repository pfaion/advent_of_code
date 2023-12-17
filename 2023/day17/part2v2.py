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
