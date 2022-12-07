# Day 2

[Exercise Text](https://adventofcode.com/2015/day/2)

## Part 1
```python
from itertools import starmap
from pathlib import Path

here = Path(__file__).parent
data: list[tuple[int, int, int]] = [
    map(int, line.split("x")) for line in (here / "input.txt").read_text().splitlines()
]


def required_paper(l: int, w: int, h: int) -> int:
    sides = (l * w, w * h, h * l)
    paper = 2 * sum(sides) + min(sides)
    return paper


print(sum(starmap(required_paper, data)))

```
Runtime: 0.037s, Size: 400, Output:
```
1606483
```
## Part 2
```python
from math import prod
from pathlib import Path

here = Path(__file__).parent
data = (here / "input.txt").read_text().splitlines()
dimensions: list[tuple[int, int, int]] = [
    tuple(int(d) for d in line.split("x")) for line in data
]


def required_ribbon(sides: tuple[int, int, int]) -> int:
    smaller_sides = sorted(sides)[0:2]
    return 2 * sum(smaller_sides) + prod(sides)


print(sum(map(required_ribbon, dimensions)))

```
Runtime: 0.038s, Size: 428, Output:
```
3842356
```