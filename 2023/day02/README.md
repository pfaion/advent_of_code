# Day 2

[Exercise Text](https://adventofcode.com/2023/day/2)

## Part 1
```python
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

max_values = {"red": 12, "green": 13, "blue": 14}

id_sum = 0
for line in data_raw:
    prefix, sets_raw = line.split(":")
    game_id = int(prefix[5:])
    for set_raw in sets_raw.split(";"):
        for entry_raw in set_raw.split(","):
            count_str, color = entry_raw.strip().split(" ")
            count = int(count_str)
            if count > max_values.get(color, 0):
                break
        else:
            continue
        break
    else:
        id_sum += game_id

print(id_sum)

```
Runtime: 0.03s, Size: 605, Output:
```
2632
```
## Part 2
```python
import re
from collections import defaultdict
from math import prod
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

power_sum = 0
for line in data_raw:
    min_cubes = defaultdict(int)
    entries: list[tuple[str, str]] = re.findall(r"(\d+) (red|green|blue)", line)
    for entry in entries:
        count = int(entry[0])
        color = entry[1]
        min_cubes[color] = max(min_cubes[color], count)
    power_sum += prod(min_cubes.values())
print(power_sum)

```
Runtime: 0.022s, Size: 515, Output:
```
69629
```