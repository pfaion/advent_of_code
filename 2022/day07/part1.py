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
