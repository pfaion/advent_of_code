from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()

head = [0, 0]
tail = [0, 0]

tail_positions: set[tuple[int, int]] = {tuple(tail)}

for entry in data:
    direction = entry[0]
    distance = int(entry[2:])

    for _ in range(distance):

        if direction == "U":
            head[0] -= 1
        elif direction == "D":
            head[0] += 1
        elif direction == "L":
            head[1] -= 1
        elif direction == "R":
            head[1] += 1

        if any(abs(h - t) > 1 for h, t in zip(head, tail)):
            tail[0] += min(1, max(-1, head[0] - tail[0]))
            tail[1] += min(1, max(-1, head[1] - tail[1]))

        tail_positions.add(tuple(tail))

print(len(tail_positions))
