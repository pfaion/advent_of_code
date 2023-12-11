from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()
# padding to avoid bounds checking
width = len(data_raw[0]) + 2
pipes = ["." * width] + ["." + line + "." for line in data_raw] + ["." * width]

start = next(
    (rowi, coli)
    for rowi, row in enumerate(pipes)
    for coli, cell in enumerate(row)
    if cell == "S"
)

row_prev, col_prev = start
direction, row, col = next(
    (direction, row, col)
    for direction, row, col in (
        ("u", row_prev - 1, col_prev),
        ("d", row_prev + 1, col_prev),
        ("l", row_prev, col_prev - 1),
        ("r", row_prev, col_prev + 1),
    )
    if direction + pipes[row][col] in "u7u|uFdJd|dLlLl-lFrJr-r7"
)

length = 1
while (row, col) != start:
    state = direction + pipes[row][col]
    if state in "rJu|lL":
        direction = "u"
        row -= 1
    elif state in "r7d|lF":
        direction = "d"
        row += 1
    elif state in "dJl-u7":
        direction = "l"
        col -= 1
    elif state in "dLr-uF":
        direction = "r"
        col += 1
    length += 1

print(length // 2)
