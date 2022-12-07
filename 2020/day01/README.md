# Day 1

[Exercise Text](https://adventofcode.com/2020/day/1)

## Part 1
```python
from math import prod
from pathlib import Path
from typing import Sequence

here = Path(__file__).parent


def find_summands(data: Sequence[int], target: int) -> tuple[int, int]:
    for idx, a in enumerate(data):
        for b in data[idx + 1 :]:
            if a + b == target:
                return (a, b)
    raise ValueError("Could not create target sum from data.")


# assert find_summands((1721, 979, 366, 299, 675, 1456), 2020) == (1721, 299)


data = list(map(int, (here / "input.txt").read_text().splitlines()))
print(prod(find_summands(data, 2020)))

```
Runtime: 0.042s, Size: 563, Output:
```
960075
```
## Part 2