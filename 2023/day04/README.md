# Day 4

[Exercise Text](https://adventofcode.com/2023/day/4)

## Part 1
```python
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

# I'm sorry.
print(
    sum(
        2 ** (n_winning - 1)
        for line in data_raw
        if (
            n_winning := len(
                set.intersection(
                    *map(lambda s: set(s.split()), line.split(": ")[1].split(" | "))
                )
            )
        )
        > 0
    )
)

```
Runtime: 0.031s, Size: 412, Output:
```
27059
```
## Part 2
```python
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

n_cards = len(data_raw)
card_counts = {i: 1 for i in range(n_cards)}

for i, line in enumerate(data_raw):
    n_winning = len(
        set.intersection(
            *map(lambda s: set(s.split()), line.split(": ")[1].split(" | "))
        )
    )
    current_count = card_counts[i]
    for offset in range(1, n_winning + 1):
        if (duplication_i := i + offset) in card_counts:
            card_counts[duplication_i] += current_count

print(sum(card_counts.values()))

```
Runtime: 0.022s, Size: 572, Output:
```
5744979
```