from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()

rope = [[0, 0] for _ in range(10)]

tail_positions: set[tuple[int, int]] = {tuple(rope[-1])}

for entry in data:
    direction = entry[0]
    distance = int(entry[2:])

    for _ in range(distance):

        if direction == "U":
            rope[0][0] -= 1
        elif direction == "D":
            rope[0][0] += 1
        elif direction == "L":
            rope[0][1] -= 1
        elif direction == "R":
            rope[0][1] += 1

        for i in range(1, len(rope)):
            if any(abs(h - t) > 1 for h, t in zip(rope[i - 1], rope[i])):
                rope[i][0] += min(1, max(-1, rope[i - 1][0] - rope[i][0]))
                rope[i][1] += min(1, max(-1, rope[i - 1][1] - rope[i][1]))

        tail_positions.add(tuple(rope[-1]))

print(len(tail_positions))
