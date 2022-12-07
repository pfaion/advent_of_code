# Day 1

[Exercise Text](https://adventofcode.com/2015/day/1)

## Part 1
```python
from pathlib import Path

here = Path(__file__).parent


def get_floor(data: str) -> int:
    return sum(1 if char == "(" else -1 for char in data)


# assert get_floor("(())") == 0
# assert get_floor("()()") == 0
# assert get_floor("(((") == 3
# assert get_floor("(()(()(") == 3
# assert get_floor("))(((((") == 3
# assert get_floor("())") == -1
# assert get_floor("))(") == -1
# assert get_floor(")))") == -3
# assert get_floor(")())())") == -3


data = (here / "input.txt").read_text()
print(get_floor(data))

```
Runtime: 0.035s, Size: 512, Output:
```
232
```
## Part 2
```python
from itertools import accumulate, takewhile
from pathlib import Path

here = Path(__file__).parent


def first_basement_enter(data: str) -> int:
    floors = accumulate(1 if char == "(" else -1 for char in data)
    floors_before_basement = takewhile(lambda x: x >= 0, floors)
    return len(list(floors_before_basement)) + 1


# assert first_basement_enter(")") == 1
# assert first_basement_enter("()())") == 5


data = (here / "input.txt").read_text()
print(first_basement_enter(data))

```
Runtime: 0.038s, Size: 488, Output:
```
1783
```