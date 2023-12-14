# Day 14

[Exercise Text](https://adventofcode.com/2023/day/14)

## Part 1
```python
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

height = len(data_raw)
columns = list(zip(*data_raw))
total_load = 0
for column in columns:
    n_free_above = 0
    for i, cell in enumerate(column):
        if cell == "O":
            final_position = i - n_free_above
            load = height - final_position
            total_load += load
        elif cell == ".":
            n_free_above += 1
        elif cell == "#":
            n_free_above = 0
print(total_load)

```
Runtime: 0.026s, Size: 525, Output:
```
105003
```
## Part 2
```python
from copy import deepcopy
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()


type Lines = list[list[str]]


def rotate_right(lines: Lines) -> Lines:
    return [list(reversed(line)) for line in zip(*lines)]


def shift_left(lines: Lines) -> Lines:
    height = len(lines)
    width = len(lines[0])
    for line_i in range(height):
        line = lines[line_i]
        n_free_above = 0
        for cell_i in range(width):
            cell = line[cell_i]
            if cell == "O":
                final_position = cell_i - n_free_above
                line[cell_i] = "."
                line[final_position] = "O"
            elif cell == ".":
                n_free_above += 1
            elif cell == "#":
                n_free_above = 0
    return lines


def calculate_left_load(lines: Lines) -> int:
    width = len(lines[0])
    return sum(
        sum(width - i for i, cell in enumerate(line) if cell == "O") for line in lines
    )


lines = data_raw
for _ in range(3):
    lines = rotate_right(lines)
# north is left
cycle = 0
target = 1000000000
loop_check = [deepcopy(lines)]
while cycle < target:
    for direction in range(4):
        lines = shift_left(lines)
        lines = rotate_right(lines)
    # north is left again
    cycle += 1

    if loop_check is None:
        continue

    if lines not in loop_check:
        loop_check.append(deepcopy(lines))
        continue

    loop_start = loop_check.index(lines)
    loop_length = len(loop_check) - loop_start
    remaining = target - cycle
    skip_loops = remaining // loop_length
    cycle += skip_loops * loop_length
    loop_check = None

print(calculate_left_load(lines))

```
Runtime: 0.503s, Size: 1698, Output:
```
93742
```