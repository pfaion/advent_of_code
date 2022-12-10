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
