# Day 5

[Exercise Text](https://adventofcode.com/2022/day/5)

## Part 1
```python
import re
from pathlib import Path

stacks_raw, moves_raw = Path(__file__).with_name("input.txt").read_text().split("\n\n")

# initialize a list of empty stacks
n_stacks = stacks_raw.find("\n") // 4 + 1
stacks = [[] for _ in range(n_stacks)]

# parse stack data
for line in stacks_raw.splitlines()[:-1]:
    for stack_idx, crate in enumerate(line[1::4]):
        if crate != " ":
            stacks[stack_idx].insert(0, crate)

# process move data
for line in moves_raw.splitlines():
    match = re.match(r"move (\d+) from (\d+) to (\d+)", line)
    n_move, source, target = map(int, match.groups())
    for _ in range(n_move):
        stacks[target - 1].append(stacks[source - 1].pop())

print("".join(stack[-1] for stack in stacks))

```
Runtime: 0.044s, Size: 735, Output:
```
TGWSMRBPN
```
## Part 2
```python
import re
from pathlib import Path

stacks_raw, moves_raw = Path(__file__).with_name("input.txt").read_text().split("\n\n")

# initialize a list of empty stacks
n_stacks = stacks_raw.find("\n") // 4 + 1
stacks = [[] for _ in range(n_stacks)]

# parse stack data
for line in stacks_raw.splitlines()[:-1]:
    for stack_idx, crate in enumerate(line[1::4]):
        if crate != " ":
            stacks[stack_idx].insert(0, crate)

# process move data
for line in moves_raw.splitlines():
    match = re.match(r"move (\d+) from (\d+) to (\d+)", line)
    n_move, source, target = map(int, match.groups())
    dummy = []
    for _ in range(n_move):
        dummy.append(stacks[source - 1].pop())
    for _ in range(n_move):
        stacks[target - 1].append(dummy.pop())


print("".join(stack[-1] for stack in stacks))

```
Runtime: 0.034s, Size: 813, Output:
```
TZLTLWRNF
```