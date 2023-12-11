import re
from itertools import cycle
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text()

lr_instruction, maps_raw = data_raw.split("\n\n")
regex = re.compile(r"\w+")
maps = {
    source: (left, right)
    for (source, left, right) in map(regex.findall, maps_raw.splitlines())
}

current = "AAA"
for step, direction in enumerate(cycle(lr_instruction), 1):
    current = maps[current][direction == "R"]
    if current == "ZZZ":
        print(step)
        break
