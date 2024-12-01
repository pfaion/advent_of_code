from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text()

current = (0, 0)
visited = {current}
for move in data_raw:
    x, y = current
    match move:
        case ">":
            current = (x + 1, y)
        case "v":
            current = (x, y - 1)
        case "<":
            current = (x - 1, y)
        case "^":
            current = (x, y + 1)
    visited.add(current)

print(len(visited))
