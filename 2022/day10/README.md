# Day 10

[Exercise Text](https://adventofcode.com/2022/day/10)

## Part 1
```python
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()

cycle_time = {"noop": 1, "addx": 2}

x = 1
cycle = 1
target_sum = 0
for line in data:
    op = line[:4]
    for _ in range(cycle_time[op]):
        # during this cycle
        if cycle == 20 or (cycle > 20 and (cycle - 20) % 40 == 0):
            target_sum += cycle * x

        # cycle completes
        cycle += 1

    # after the last op cycle completes
    if op == "addx":
        value = int(line[5:])
        x += value

print(target_sum)

```
Runtime: 0.034s, Size: 544, Output:
```
16060
```
## Part 2
```python
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()

cycle_time = {"noop": 1, "addx": 2}

sprite_x = 1
crt_x = 0
cycle = 1
for line in data:
    op = line[:4]
    for _ in range(cycle_time[op]):
        # during this cycle
        if sprite_x - 1 <= crt_x <= sprite_x + 1:
            print("█", end="")
        else:
            print(" ", end="")

        if cycle % 40 == 0:
            print("")
            crt_x = 0
        else:
            crt_x += 1

        # cycle completes
        cycle += 1

    # after the last op cycle completes
    if op == "addx":
        value = int(line[5:])
        sprite_x += value

```
Runtime: 0.035s, Size: 667, Output:
```
███   ██   ██  ████ █  █ █    █  █ ████ 
█  █ █  █ █  █ █    █ █  █    █  █ █    
███  █  █ █    ███  ██   █    ████ ███  
█  █ ████ █    █    █ █  █    █  █ █    
█  █ █  █ █  █ █    █ █  █    █  █ █    
███  █  █  ██  ████ █  █ ████ █  █ █
```