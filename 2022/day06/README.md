# Day 6

[Exercise Text](https://adventofcode.com/2022/day/6)

## Part 1
```python
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().strip()

for end in range(4, len(data)):
    chunk = data[end - 4 : end]
    if len(set(chunk)) == 4:
        print(end)
        break

```
Runtime: 0.037s, Size: 218, Output:
```
1779
```
## Part 2
```python
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().strip()

for end in range(14, len(data)):
    chunk = data[end - 14 : end]
    if len(set(chunk)) == 14:
        print(end)
        break

```
Runtime: 0.037s, Size: 221, Output:
```
2635
```