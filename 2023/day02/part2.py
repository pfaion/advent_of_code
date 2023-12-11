import re
from collections import defaultdict
from math import prod
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

power_sum = 0
for line in data_raw:
    min_cubes = defaultdict(int)
    entries: list[tuple[str, str]] = re.findall(r"(\d+) (red|green|blue)", line)
    for entry in entries:
        count = int(entry[0])
        color = entry[1]
        min_cubes[color] = max(min_cubes[color], count)
    power_sum += prod(min_cubes.values())
print(power_sum)
