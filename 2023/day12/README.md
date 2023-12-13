# Day 12

[Exercise Text](https://adventofcode.com/2023/day/12)

## Part 1
```python
import re
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

conditions, groups_raw = zip(*(line.split() for line in data_raw))
groups = [line.split(",") for line in groups_raw]

result = 0
for condition, group in zip(conditions, groups):
    pattern = re.compile(
        r"^[\.\?]*" + r"[\.\?]+".join(r"[#\?]{" + n + r"}" for n in group) + r"[\.\?]*$"
    )
    stack = [condition]
    line_result = 0
    while stack:
        assignment: str = stack.pop()
        if not pattern.match(assignment):
            continue
        if "?" not in assignment:
            line_result += 1
            continue
        stack.append(re.sub(r"\?", ".", assignment, count=1))
        stack.append(re.sub(r"\?", "#", assignment, count=1))
    result += line_result

print(result)

```
Runtime: 0.146s, Size: 821, Output:
```
7694
```
## Part 2
```python
from dataclasses import dataclass, field
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

all_conditions, groups_raw = zip(*(line.split() for line in data_raw))
all_groups = [[int(v) for v in tuple(line.split(","))] for line in groups_raw]


@dataclass
class Solver:
    conditions: str
    groups: tuple[int]
    cache: dict[tuple[int, int], int] = field(default_factory=dict)

    def possible_assignments(self, condition_i: int, group_i: int, indent=0) -> int:
        key = (condition_i, group_i)
        if key not in self.cache:
            self.cache[key] = self._possible_assignments(*key, indent)
        return self.cache[key]

    def print(self, condition_i: int, group_i: int, indent=0, result=None):
        return
        prefix = "|" * indent
        if result is None:
            print(f"{prefix}{self.conditions} [{",".join(map(str,self.groups))}]")
        else:
            print(
                f"{prefix}{self.conditions} [{",".join(map(str,self.groups))}] -> {result}"
            )
        group_str_lengths = [len(str(group)) for group in self.groups]
        print(
            f"{prefix}{" "*condition_i}^{" " * (len(self.conditions) - condition_i)} {" " * (sum(group_str_lengths[:group_i]) + group_i)}^"
        )

    def _possible_assignments(self, condition_i: int, group_i: int, indent=0) -> int:
        if group_i >= len(self.groups):
            if "#" in self.conditions[condition_i:]:
                return 0
            else:
                return 1

        group_size = self.groups[group_i]
        n_remaining_conditions = len(self.conditions) - condition_i
        max_group_right_shift = n_remaining_conditions - group_size
        result = 0
        for offset in range(0, max_group_right_shift + 1):
            start_i = condition_i + offset
            end_i = start_i + group_size

            group_fits = True
            for char in self.conditions[start_i:end_i]:
                if char not in "#?":
                    group_fits = False
                    break
            if self.conditions[end_i : end_i + 1] not in ".?":
                group_fits = False

            if group_fits:
                self.print(start_i, group_i, indent)
                x = self.possible_assignments(end_i + 1, group_i + 1, indent + 1)
                self.print(start_i, group_i, indent, x)
                result += x

            if self.conditions[start_i : start_i + 1] == "#":
                break

        return result


repeat = 5
result = 0
for i, (conditions, groups) in enumerate(zip(all_conditions, all_groups)):
    conditions = "?".join(conditions for _ in range(repeat))
    groups = groups * repeat
    line_result = Solver(conditions, groups).possible_assignments(0, 0)
    result += line_result

print(result)

```
Runtime: 0.598s, Size: 2829, Output:
```
5071883216318
```