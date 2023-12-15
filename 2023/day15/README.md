# Day 15

[Exercise Text](https://adventofcode.com/2023/day/15)

## Part 1
```python
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().strip()


def compute_hash(string: str) -> int:
    value = 0
    for character in string:
        value += ord(character)
        value *= 17
        value = value % 256
    return value


assert compute_hash("HASH") == 52
assert compute_hash("rn=1") == 30

initialization_sequence = data_raw.split(",")
print(sum(compute_hash(step) for step in initialization_sequence))

```
Runtime: 0.032s, Size: 459, Output:
```
517015
```
## Part 2
```python
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().strip()


def compute_hash(string: str) -> int:
    value = 0
    for character in string:
        value += ord(character)
        value *= 17
        value = value % 256
    return value


@dataclass
class Lens:
    label: str
    focal_length: int


Box = list[Lens]

boxes: dict[int, Box] = defaultdict(Box)

initialization_sequence = data_raw.split(",")

parser = re.compile(r"(?P<label>\w+)(?P<operation>=|-)(?P<focal_length>\d+)?")
for step in initialization_sequence:
    match parser.match(step).groups():
        case (label, "=", focal_length):
            focal_length = int(focal_length)
            box_number = compute_hash(label)
            box = boxes[box_number]
            for lens in box:
                if lens.label == label:
                    lens.focal_length = focal_length
                    break
            else:
                box.append(Lens(label, focal_length))
        case (label, "-", _):
            box_number = compute_hash(label)
            box = boxes[box_number]
            for lens in box:
                if lens.label == label:
                    box.remove(lens)
                    break

print(
    sum(
        (1 + box_number) * slot_number * lens.focal_length
        for box_number, box in boxes.items()
        for slot_number, lens in enumerate(box, 1)
    )
)

```
Runtime: 0.034s, Size: 1491, Output:
```
286104
```