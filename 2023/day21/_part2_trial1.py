from pathlib import Path

from rich import print
from rich.console import Console

data = Path(__file__).with_name("input.txt").read_text().splitlines()
height = len(data)
width = len(data[0])

start = next(
    (row, col)
    for row, line in enumerate(data)
    for col, cell in enumerate(line)
    if cell == "S"
)


def get_neightbors(row: int, col: int) -> list[tuple[int, int]]:
    return [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]


console = Console()

current = {start}
for i in range(500):
    current = {
        (nrow, ncol)
        for row, col in current
        for nrow, ncol in get_neightbors(row, col)
        if data[nrow % height][ncol % width] != "#"
    }

    if (i + 1) % 10 == 0:
        console.print(i + 1, "->", len(current))

    # minrow = min(row for row, col in current)
    # mincol = min(col for row, col in current)
    # maxrow = max(row for row, col in current)
    # maxcol = max(col for row, col in current)
    # for row in range(minrow - 1, maxrow + 2):
    #     for col in range(mincol - 1, maxcol + 2):
    #         if (row, col) in current:
    #             console.print(" ", style="on red", end="")
    #         else:
    #             cell = data[row % height][col % width]
    #             if cell in "S.":
    #                 console.print(" ", style="on green", end="")
    #             else:
    #                 console.print(" ", style="on black", end="")
    #     console.print()
