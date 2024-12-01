from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text()

states = [(0, 0), (0, 0)]
visited = {(0, 0)}
active_index = 0
for move in data_raw:
    x, y = states[active_index]
    match move:
        case ">":
            states[active_index] = (x + 1, y)
        case "v":
            states[active_index] = (x, y - 1)
        case "<":
            states[active_index] = (x - 1, y)
        case "^":
            states[active_index] = (x, y + 1)
    visited.add(states[active_index])
    active_index = (active_index + 1) % 2

print(len(visited))
