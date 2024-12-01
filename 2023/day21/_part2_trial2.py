from collections import Counter
from pathlib import Path

from rich import print
from rich.console import Console

data = Path(__file__).with_name("input.txt").read_text().splitlines()
height = len(data)
width = len(data[0])

type Point = tuple[int, int]
start: Point = next(
    (row, col)
    for row, line in enumerate(data)
    for col, cell in enumerate(line)
    if cell == "S"
)


def get_neightbors(row: int, col: int) -> list[tuple[int, int]]:
    return [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]


def get_quadrant(row: int, col: int) -> int:
    quad_row = 0 if row < 0 else 1 if row < height else 2
    quad_col = 0 if col < 0 else 1 if col < width else 2
    return quad_row * 3 + quad_col


type Pattern = frozenset[Point]


def propagate(pattern: Pattern, n: int) -> list[Pattern]:
    new_points = set(pattern)
    for _ in range(n):
        new_points = {
            (nrow, ncol)
            for row, col in new_points
            for nrow, ncol in get_neightbors(row, col)
            if data[nrow % height][ncol % width] != "#"
        }
    quadrants = [set() for _ in range(9)]
    for row, col in new_points:
        quadrants[get_quadrant(row, col)].add((row % height, col % width))
    return [frozenset(quad_set) for quad_set in quadrants if quad_set]


console = Console()


# propagate ONCE, to get a start of 1
initial = {start}
# tmp = propagate(initial, 1)
# assert len(tmp) == 1
# initial = tmp[0]

current: dict[Pattern:int] = Counter({frozenset(initial): 1})
for i in range(1, 11, 1):
    new = Counter()
    for pattern, count in current.items():
        for expansion in propagate(pattern, 1):
            new[expansion] += count
    current = new

    console.print()
    console.print("=" * 20, i, "=" * 20)
    for pattern, count in current.items():
        console.print(f"Pattern ({count=}): {len(pattern)=}")
        for row in range(height):
            for col in range(width):
                if (row, col) in pattern:
                    console.print(" ", style="on red", end="")
                else:
                    cell = data[row][col]
                    if cell in "S.":
                        console.print(" ", style="on green", end="")
                    else:
                        console.print(" ", style="on black", end="")
            console.print()
