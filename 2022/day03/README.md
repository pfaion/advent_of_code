# Day 3

[Exercise Text](https://adventofcode.com/2022/day/3)

## Part 1
```python
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()


def find_wrong_item(items: str) -> str:
    mid = len(items) // 2
    first_compartment = items[:mid]
    second_compartment = items[mid:]
    overlapping_items = set(first_compartment) & set(second_compartment)
    return next(iter(overlapping_items))


def item_priority(item: str) -> int:
    code = ord(item)
    # capitals come before lowercase in ascii codes
    if code <= ord("Z"):
        return code - ord("A") + 27
    else:
        return code - ord("a") + 1


print(sum(item_priority(find_wrong_item(items)) for items in data))

```
Runtime: 0.038s, Size: 639, Output:
```
7908
```
## Part 2
```python
import re
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text()

batches = [
    match[0] for match in re.finditer(r"\w+\n\w+\n\w+(\n|$)", data_raw, re.MULTILINE)
]


def find_badge(batch: str) -> str:
    elf_items = batch.splitlines()
    overlap = set.intersection(*(set(items) for items in elf_items))
    return next(iter(overlap))


def item_priority(item: str) -> int:
    code = ord(item)
    # capitals come before lowercase in ascii codes
    if code <= ord("Z"):
        return code - ord("A") + 27
    else:
        return code - ord("a") + 1


print(sum(item_priority(find_badge(batch)) for batch in batches))

```
Runtime: 0.038s, Size: 656, Output:
```
2838
```