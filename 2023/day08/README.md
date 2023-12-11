# Day 8

[Exercise Text](https://adventofcode.com/2023/day/8)

## Part 1
```python
import re
from itertools import cycle
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text()

lr_instruction, maps_raw = data_raw.split("\n\n")
regex = re.compile(r"\w+")
maps = {
    source: (left, right)
    for (source, left, right) in map(regex.findall, maps_raw.splitlines())
}

current = "AAA"
for step, direction in enumerate(cycle(lr_instruction), 1):
    current = maps[current][direction == "R"]
    if current == "ZZZ":
        print(step)
        break

```
Runtime: 0.03s, Size: 497, Output:
```
22411
```
## Part 2
```python
import re
from math import lcm
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text()

lr_instruction, maps_raw = data_raw.split("\n\n")
regex = re.compile(r"\w+")
maps = {
    source: (left, right)
    for (source, left, right) in map(regex.findall, maps_raw.splitlines())
}


def find_zero_aligned_path(start: str) -> list[bool]:
    current = start
    path = []
    while True:
        iindex = 0
        if (current, iindex) in path:
            path_start = path.index((current, iindex))
            return [part.endswith("Z") for part, _ in path[path_start:]]
        for iindex in range(len(lr_instruction)):
            path.append((current, iindex))
            direction = lr_instruction[iindex]
            current = maps[current][direction == "R"]


starts = [source for source in maps if source.endswith("A")]
paths = list(map(find_zero_aligned_path, starts))
full_loop_length = lcm(*map(len, paths))
# WAT?? why does this work? lucky guess
print(full_loop_length)

```
Runtime: 0.095s, Size: 1011, Output:
```
11188774513823
```