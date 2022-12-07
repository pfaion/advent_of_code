# Day 7

[Exercise Text](https://adventofcode.com/2022/day/7)

## Part 1
```python
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()

tree = {}
trace = [tree]
for line in data[1:]:
    current = trace[-1]
    if line.startswith("$ ls"):
        continue
    elif line.startswith("$ cd"):
        name = line[5:]
        if name == "..":
            trace.pop()
        else:
            trace.append(current[name])
    elif line.startswith("dir"):
        name = line[4:]
        current[name] = {}
    else:
        parts = line.split(" ")
        size = int(parts[0])
        name = parts[1]
        current[name] = size


target_sum = 0


def get_directory_size(dir: dict) -> int:
    global target_sum
    size = sum(
        child if isinstance(child, int) else get_directory_size(child)
        for child in dir.values()
    )
    if size <= 100000:
        target_sum += size
    return size


get_directory_size(tree)
print(target_sum)

```
Runtime: 0.027s, Size: 907, Output:
```
1423358
```
## Part 2
```python
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()

tree = {}
trace = [tree]
for line in data[1:]:
    current = trace[-1]
    if line.startswith("$ ls"):
        continue
    elif line.startswith("$ cd"):
        name = line[5:]
        if name == "..":
            trace.pop()
        else:
            trace.append(current[name])
    elif line.startswith("dir"):
        name = line[4:]
        current[name] = {}
    else:
        parts = line.split(" ")
        size = int(parts[0])
        name = parts[1]
        current[name] = size


all_directory_sizes = []


def get_directory_size(dir: dict) -> int:
    global all_directory_sizes
    size = sum(
        child if isinstance(child, int) else get_directory_size(child)
        for child in dir.values()
    )
    all_directory_sizes.append(size)
    return size


root_size = get_directory_size(tree)
current_free_space = 70000000 - root_size
min_deletion_size = 30000000 - current_free_space

for dir_size in sorted(all_directory_sizes):
    if dir_size >= min_deletion_size:
        print(dir_size)
        break

```
Runtime: 0.032s, Size: 1121, Output:
```
545729
```