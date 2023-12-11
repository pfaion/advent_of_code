import re
from math import lcm
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text()

lr_instruction, maps_raw = data_raw.split("\n\n")
regex = re.compile(r"\w+")
maps = {
    source: (left, right)
    for (source, left, right) in map(regex.findall, maps_raw.splitlines())
}


def find_zero_aligned_path(start: str) -> list[bool]:
    current = start
    path = []
    while True:
        iindex = 0
        if (current, iindex) in path:
            path_start = path.index((current, iindex))
            return [part.endswith("Z") for part, _ in path[path_start:]]
        for iindex in range(len(lr_instruction)):
            path.append((current, iindex))
            direction = lr_instruction[iindex]
            current = maps[current][direction == "R"]


starts = [source for source in maps if source.endswith("A")]
paths = list(map(find_zero_aligned_path, starts))
full_loop_length = lcm(*map(len, paths))
# WAT?? why does this work? lucky guess
print(full_loop_length)
