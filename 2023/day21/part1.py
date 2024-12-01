from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()
width = len(data_raw[0]) + 2
data = ["#" * width] + ["#" + line + "#" for line in data_raw] + ["#" * width]

start = next(
    (row, col)
    for row, line in enumerate(data)
    for col, cell in enumerate(line)
    if cell == "S"
)


def get_neightbors(row: int, col: int) -> list[tuple[int, int]]:
    return [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]


current = {start}
for i in range(64):
    current = {
        (nrow, ncol)
        for row, col in current
        for nrow, ncol in get_neightbors(row, col)
        if data[nrow][ncol] != "#"
    }

print(len(current))
