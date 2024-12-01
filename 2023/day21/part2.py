from itertools import pairwise
from pathlib import Path

from rich import print
from rich.console import Console
from tqdm import trange

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

prev = set()
current = {start}
even = 1
odd = 0

areas = []
steps = [1]
i = 1
while True:
    new = {
        (nrow, ncol)
        for row, col in current
        for nrow, ncol in get_neightbors(row, col)
        if data[nrow % height][ncol % width] != "#" and (nrow, ncol) not in prev
    }

    if i % 2 == 0:
        even += len(new)
        total = even
    else:
        odd += len(new)
        total = odd

    console.print()
    console.print(i, f"{len(current)=}", f"{total=}")

    prev = current
    current = new

    if len(areas) == 0 and (0, start[1]) in current:
        # we captured the inner filled rhombus
        # ◸╱◢◣╲◹
        # ◺╲◥◤╱◿
        areas.append(total)
        steps.append(i)
        # minrow = min(row for row, col in current)
        # mincol = min(col for row, col in current)
        # maxrow = max(row for row, col in current)
        # maxcol = max(col for row, col in current)
        # for row in range(minrow - 1, maxrow + 1):
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

    if len(areas) == 1 and (-height, start[1]) in current:
        # captures the next bigger rhombus
        #  ◢◣ ◹◸╱◢◣╲◹◸ ◢◣
        #  ◥◤╱◿◺ ◥◤ ◿◺╲◥◤
        # ╱◢◣ ◹◸ ◢◣ ◹◸ ◢◣╲
        # ╲◥◤ ◿◺ ◥◤ ◿◺ ◥◤╱
        #  ◢◣╲◹◸ ◢◣ ◹◸╱◢◣
        #  ◥◤ ◿◺╲◥◤╱◿◺ ◥◤
        areas.append((total - 5 * areas[0]) / 4)
        steps.append(i)
        # minrow = min(row for row, col in current)
        # mincol = min(col for row, col in current)
        # maxrow = max(row for row, col in current)
        # maxcol = max(col for row, col in current)
        # for row in range(minrow - 1, maxrow + 1):
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

    if len(areas) == 2 and (-2 * height, start[1]) in current:
        # captures the next bigger rhombus
        #  ◢◣ ◹◸ ◢◣ ◹◸╱◢◣╲◹◸ ◢◣ ◹◸ ◢◣
        #  ◥◤ ◿◺ ◥◤╱◿◺ ◥◤ ◿◺╲◥◤ ◿◺ ◥◤
        #  ◢◣ ◹◸╱◢◣ ◹◸ ◢◣ ◹◸ ◢◣╲◹◸ ◢◣
        #  ◥◤╱◿◺ ◥◤ ◿◺ ◥◤ ◿◺ ◥◤ ◿◺╲◥◤
        # ╱◢◣ ◹◸ ◢◣ ◹◸ ◢◣ ◹◸ ◢◣ ◹◸ ◢◣╲
        # ╲◥◤ ◿◺ ◥◤ ◿◺ ◥◤ ◿◺ ◥◤ ◿◺ ◥◤╱
        #  ◢◣╲◹◸ ◢◣ ◹◸ ◢◣ ◹◸ ◢◣ ◹◸╱◢◣
        #  ◥◤ ◿◺╲◥◤ ◿◺ ◥◤ ◿◺ ◥◤╱◿◺ ◥◤
        #  ◢◣ ◹◸ ◢◣╲◹◸ ◢◣ ◹◸╱◢◣ ◹◸ ◢◣
        #  ◥◤ ◿◺ ◥◤ ◿◺╲◥◤╱◿◺ ◥◤ ◿◺ ◥◤
        # minrow = min(row for row, col in current)
        # mincol = min(col for row, col in current)
        # maxrow = max(row for row, col in current)
        # maxcol = max(col for row, col in current)
        # for row in range(minrow - 1, maxrow + 1):
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
        steps.append(i)
        break

    i += 1
print(areas)
print(steps)
print([b - a for a, b in pairwise(steps)])
