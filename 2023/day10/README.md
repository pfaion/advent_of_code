# Day 10

[Exercise Text](https://adventofcode.com/2023/day/10)

## Part 1
```python
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

```
Runtime: 0.033s, Size: 1105, Output:
```
6820
```
## Part 2
```python
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()
# padding to avoid bounds checking
width = len(data_raw[0]) + 2
pipes = ["." * width] + ["." + line + "." for line in data_raw] + ["." * width]
height = len(pipes)

# find start
start = next(
    (rowi, coli)
    for rowi, row in enumerate(pipes)
    for coli, cell in enumerate(row)
    if cell == "S"
)

# find outgoing pipes from start
row_prev, col_prev = start
start_neighbors = [
    (direction, row, col)
    for direction, row, col in (
        ("u", row_prev - 1, col_prev),
        ("d", row_prev + 1, col_prev),
        ("l", row_prev, col_prev - 1),
        ("r", row_prev, col_prev + 1),
    )
    if direction + pipes[row][col] in "u7u|uFdJd|dLlLl-lFrJr-r7"
]

# replace S with proper start pipe (for inside logic)
start_neighbor_directions = "".join(
    sorted(direction for direction, *_ in start_neighbors)
)
start_pipe = {"dl": "7", "dr": "F", "du": "|", "lr": "-", "lu": "J", "ru": "L"}[
    start_neighbor_directions
]
pipes[row_prev] = pipes[row_prev].replace("S", start_pipe)

# find loop
direction, row, col = start_neighbors[0]
loop = [start, (row, col)]
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
    loop.append((row, col))

# process inside logic, this is basically the point-in-polygon raycasting algorithm
n_enclosed = 0
for row in range(height):
    inside = False
    segment_start = None
    for col in range(width):
        if (row, col) in loop:
            pipe = pipes[row][col]
            if pipe == "|":
                inside ^= True
            elif (segment_start, pipe) in ((None, "L"), (None, "F")):
                segment_start = pipe
            elif (segment_start, pipe) in (("L", "J"), ("F", "7")):
                segment_start = None
            elif (segment_start, pipe) in (("L", "7"), ("F", "J")):
                segment_start = None
                inside ^= True
        elif inside:
            n_enclosed += 1

print(n_enclosed)

```
Runtime: 2.259s, Size: 2289, Output:
```
337
```