# Day 7

[Exercise Text](https://adventofcode.com/2022/day/7)

## Part 1
### Overview
| Variant | Runtime | Size |
| --- | --- | --- |
|1|0.039s|907|
|2|0.04s|554|

### Variant 1
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
Runtime: 0.039s, Size: 907, Output:
```
1423358
```
### Variant 2
```python
from collections import Counter
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()

dir_sizes: dict[str, int] = Counter()
trace = [""]
for line in data[1:]:
    if line == "$ cd ..":
        trace.pop()
    elif line.startswith("$ cd"):
        trace.append(line[5:])
    elif line[0].isnumeric():
        parts = line.split(" ")
        for dir in Path("/".join(trace + [parts[1]])).parents:
            dir_sizes[str(dir)] += int(parts[0])

print(sum(size for size in dir_sizes.values() if size <= 100000))

```
Runtime: 0.04s, Size: 554, Output:
```
1423358
```
## Part 2
### Overview
| Variant | Runtime | Size |
| --- | --- | --- |
|1|0.027s|1121|
|2|0.035s|671|

### Variant 1
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
Runtime: 0.027s, Size: 1121, Output:
```
545729
```
### Variant 2
```python
from collections import Counter
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()

dir_sizes: dict[str, int] = Counter()
trace = [""]
for line in data[1:]:
    if line == "$ cd ..":
        trace.pop()
    elif line.startswith("$ cd"):
        trace.append(line[5:])
    elif line[0].isnumeric():
        parts = line.split(" ")
        for dir in Path("/".join(trace + [parts[1]])).parents:
            dir_sizes[str(dir)] += int(parts[0])

current_free_space = 70000000 - dir_sizes["/"]
min_deletion_size = 30000000 - current_free_space
print(next(size for size in sorted(dir_sizes.values()) if size >= min_deletion_size))

```
Runtime: 0.035s, Size: 671, Output:
```
545729
```