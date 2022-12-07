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
