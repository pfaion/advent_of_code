# Day 2

[Exercise Text](https://adventofcode.com/2022/day/2)

## Part 1
### Overview
| Variant | Runtime | Size |
| --- | --- | --- |
|1|0.042s|607|
|2|0.035s|442|
|3|0.026s|250|

### Variant 1
```python
from itertools import starmap
from pathlib import Path

here = Path(__file__).parent

data = [line.split(" ") for line in (here / "input.txt").read_text().splitlines()]


def score(opponent_move: str, own_move: str) -> int:
    game_score = {
        ("A", "Z"): 0,
        ("B", "X"): 0,
        ("C", "Y"): 0,
        ("A", "X"): 3,
        ("B", "Y"): 3,
        ("C", "Z"): 3,
        ("A", "Y"): 6,
        ("B", "Z"): 6,
        ("C", "X"): 6,
    }[(opponent_move, own_move)]

    move_value = {"X": 1, "Y": 2, "Z": 3}[own_move]

    return game_score + move_value


print(sum(starmap(score, data)))

```
Runtime: 0.042s, Size: 607, Output:
```
12772
```
### Variant 2
```python
from itertools import starmap
from pathlib import Path

here = Path(__file__).parent

data = [line.split(" ") for line in (here / "input.txt").read_text().splitlines()]


def score(opponent_move: str, own_move: str) -> int:
    # computing the result based on the ascii values of the characters
    a = ord(opponent_move) - ord("A")
    b = ord(own_move) - ord("X")
    return ((b - a + 4) % 3) * 3 + b + 1


print(sum(starmap(score, data)))

```
Runtime: 0.035s, Size: 442, Output:
```
12772
```
### Variant 3
```python
from pathlib import Path

data = (Path(__file__).parent / "input.txt").read_text().splitlines()

print(
    sum(
        1
        + (b := ord((p := l.split(" "))[1]) - 88)
        + 3 * ((b + 4 - (ord(p[0]) - 65)) % 3)
        for l in data
    )
)

```
Runtime: 0.026s, Size: 250, Output:
```
12772
```
## Part 2
```python
from itertools import starmap
from pathlib import Path

here = Path(__file__).parent

data = [line.split(" ") for line in (here / "input.txt").read_text().splitlines()]


def score(opponent_move: str, outcome: str) -> int:
    own_move = {
        ("A", "X"): "C",
        ("A", "Y"): "A",
        ("A", "Z"): "B",
        ("B", "X"): "A",
        ("B", "Y"): "B",
        ("B", "Z"): "C",
        ("C", "X"): "B",
        ("C", "Y"): "C",
        ("C", "Z"): "A",
    }[(opponent_move, outcome)]

    game_score = {"X": 0, "Y": 3, "Z": 6}[outcome]
    move_value = {"A": 1, "B": 2, "C": 3}[own_move]

    return game_score + move_value


print(sum(starmap(score, data)))

```
Runtime: 0.028s, Size: 672, Output:
```
11618
```