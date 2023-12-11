# Day 6

[Exercise Text](https://adventofcode.com/2023/day/6)

## Part 1
```python
import re
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

times, distances = ([int(val) for val in re.findall(r"\d+", line)] for line in data_raw)
result = 1
for time, max_distance in zip(times, distances):
    n_ways_beating = 0
    for hold_time in range(0, time + 1):
        race_time = time - hold_time
        max_speed = hold_time
        distance = race_time * max_speed
        if distance > max_distance:
            n_ways_beating += 1
    result *= n_ways_beating
print(result)

```
Runtime: 0.03s, Size: 543, Output:
```
861300
```
## Part 2
### Overview
| Variant | Runtime | Size |
| --- | --- | --- |
|1|2.466s|330|
|2|0.02s|477|

### Variant 1
```python
import re
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

time, max_distance = (int("".join(re.findall(r"\d+", line))) for line in data_raw)

print(
    sum(
        1
        for hold_time in range(0, time + 1)
        if (time - hold_time) * hold_time > max_distance
    )
)

```
Runtime: 2.466s, Size: 330, Output:
```
28101347
```
### Variant 2
```python
import re
from math import ceil, floor, sqrt
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

time, max_distance = (int("".join(re.findall(r"\d+", line))) for line in data_raw)

# max_distance = (time - hold_time) * hold_time
# m = (t - x) * x
# x^2 - t*x + m = 0
# x = (t +- sqrt(t^2 + 4m) / 2
a = ceil((time - sqrt(time**2 - 4 * max_distance)) / 2)
b = floor((time + sqrt(time**2 - 4 * max_distance)) / 2)
print(b + 1 - a)

```
Runtime: 0.02s, Size: 477, Output:
```
28101347
```