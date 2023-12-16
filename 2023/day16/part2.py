import sys
from pathlib import Path

cave = Path(__file__).with_name("input.txt").read_text().splitlines()

height = len(cave)
width = len(cave[0])

LEFT = 1
UP = 2
RIGHT = 3
DOWN = 4

beams: list[list[set[int]]] = [[set() for _ in line] for line in cave]


def fill(row: int, col: int, direction: int):
    if not (0 <= row < height and 0 <= col < width):
        return
    if direction in beams[row][col]:
        return
    beams[row][col].add(direction)

    cell = cave[row][col]
    if (
        (direction == RIGHT and cell in ".-")
        or (direction == DOWN and cell in "\\-")
        or (direction == UP and cell in "/-")
    ):
        fill(row, col + 1, RIGHT)
    if (
        (direction == LEFT and cell in ".-")
        or (direction == DOWN and cell in "/-")
        or (direction == UP and cell in "\\-")
    ):
        fill(row, col - 1, LEFT)
    if (
        (direction == UP and cell in ".|")
        or (direction == LEFT and cell in "\\|")
        or (direction == RIGHT and cell in "/|")
    ):
        fill(row - 1, col, UP)
    if (
        (direction == DOWN and cell in ".|")
        or (direction == LEFT and cell in "/|")
        or (direction == RIGHT and cell in "\\|")
    ):
        fill(row + 1, col, DOWN)


sys.setrecursionlimit(height * width + 1)
max_energized = 0
for row in range(height):
    beams = [[set() for _ in line] for line in cave]
    fill(row, 0, RIGHT)
    n_energized = sum(1 for line in beams for cell in line if cell)
    max_energized = max(max_energized, n_energized)

    beams = [[set() for _ in line] for line in cave]
    fill(row, width - 1, LEFT)
    n_energized = sum(1 for line in beams for cell in line if cell)
    max_energized = max(max_energized, n_energized)


for col in range(width):
    beams = [[set() for _ in line] for line in cave]
    fill(0, col, DOWN)
    n_energized = sum(1 for line in beams for cell in line if cell)
    max_energized = max(max_energized, n_energized)

    beams = [[set() for _ in line] for line in cave]
    fill(height - 1, col, UP)
    n_energized = sum(1 for line in beams for cell in line if cell)
    max_energized = max(max_energized, n_energized)

print(max_energized)
