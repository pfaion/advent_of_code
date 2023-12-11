# Day 3

[Exercise Text](https://adventofcode.com/2023/day/3)

## Part 1
```python
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()
# padding to avoid bounds checking
width = len(data_raw[0]) + 2
heigth = len(data_raw) + 2
data_raw = ["." * width] + ["." + line + "." for line in data_raw] + ["." * width]

# precompute symbol-adjacent coords, as we have to compute less neighborhoods that way
type Point = tuple[int, int]
symbol_adjacent_coords: set[Point] = set()
for row, line in enumerate(data_raw):
    for col, char in enumerate(line):
        if not char.isdigit() and char != ".":
            symbol_adjacent_coords.update(
                {
                    (row - 1, col - 1),
                    (row - 1, col),
                    (row - 1, col + 1),
                    (row, col - 1),
                    (row, col + 1),
                    (row + 1, col - 1),
                    (row + 1, col),
                    (row + 1, col + 1),
                }
            )

part_number_sum = 0
for row, line in enumerate(data_raw):
    current = ""
    is_adjacent = False
    for col, char in enumerate(line):
        if not char.isdigit() and current != "":
            if is_adjacent:
                part_number_sum += int(current)
            current = ""
            is_adjacent = False
        elif char.isdigit():
            current += char
            if (row, col) in symbol_adjacent_coords:
                is_adjacent = True

print(part_number_sum)

```
Runtime: 0.029s, Size: 1443, Output:
```
539637
```
## Part 2
```python
from dataclasses import dataclass
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()
# padding to avoid bounds checking
width = len(data_raw[0]) + 2
heigth = len(data_raw) + 2
data_raw = ["." * width] + ["." + line + "." for line in data_raw] + ["." * width]

type Point = tuple[int, int]


# use unsafe hash so we can use a set later to check unique neighbor numbers.
# need to make sure we don't mutate Numbers when they are in a set
@dataclass(unsafe_hash=True)
class Number:
    start: Point
    value: int


point_to_number: dict[Point, Number] = {}
for row, line in enumerate(data_raw):
    current: Number | None = None
    for col, char in enumerate(line):
        p = (row, col)
        if char.isdigit() and current is None:
            current = Number(start=p, value=int(char))
            point_to_number[p] = current
        elif char.isdigit():
            current.value = current.value * 10 + int(char)
            point_to_number[p] = current
        elif current is not None:
            current = None

gear_ratio_sum = 0
for row, line in enumerate(data_raw):
    for col, char in enumerate(line):
        if char != "*":
            continue
        adjacent_points = {
            (row - 1, col - 1),
            (row - 1, col),
            (row - 1, col + 1),
            (row, col - 1),
            (row, col + 1),
            (row + 1, col - 1),
            (row + 1, col),
            (row + 1, col + 1),
        }
        adjacent_numbers = list(
            {point_to_number[p] for p in adjacent_points if p in point_to_number}
        )
        if len(adjacent_numbers) != 2:
            continue
        gear_ratio = adjacent_numbers[0].value * adjacent_numbers[1].value
        gear_ratio_sum += gear_ratio

print(gear_ratio_sum)

```
Runtime: 0.038s, Size: 1809, Output:
```
82818007
```