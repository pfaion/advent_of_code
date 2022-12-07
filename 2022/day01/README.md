# Day 1

[Exercise Text](https://adventofcode.com/2022/day/1)

## Part 1
```python
from pathlib import Path

here = Path(__file__).parent

raw_input = (here / "input.txt").read_text()


def max_elf_calories(raw_input: str) -> int:
    elf_calories = [
        sum(int(line) for line in elf_data_raw.splitlines())
        for elf_data_raw in raw_input.split("\n\n")
    ]
    return max(elf_calories)


print(max_elf_calories(raw_input))

```
Runtime: 0.036s, Size: 354, Output:
```
74198
```
## Part 2
```python
from pathlib import Path

here = Path(__file__).parent

raw_input = (here / "input.txt").read_text()


def max_three_elf_calories(raw_input: str) -> list[int]:
    elf_calories = [
        sum(int(line) for line in elf_data_raw.splitlines())
        for elf_data_raw in raw_input.split("\n\n")
    ]
    max_three = sorted(elf_calories)[-3:]
    return max_three


print(sum(max_three_elf_calories(raw_input)))

```
Runtime: 0.04s, Size: 411, Output:
```
209914
```