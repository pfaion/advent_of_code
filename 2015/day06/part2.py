import re
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

lights = [[0] * 1000 for _ in range(1000)]

matcher = re.compile(
    r"(?P<mode>toggle|turn on|turn off) (?P<r0>\d+),(?P<c0>\d+) \w+"
    r" (?P<r1>\d+),(?P<c1>\d+)"
)
for line in data_raw:
    mode, *coords = matcher.search(line).groups()
    row0, col0, row1, col1 = map(int, coords)
    for row in range(row0, row1 + 1):
        for col in range(col0, col1 + 1):
            match mode:
                case "turn on":
                    lights[row][col] += 1
                case "turn off":
                    lights[row][col] -= 1
                    lights[row][col] = max(0, lights[row][col])
                case "toggle":
                    lights[row][col] += 2

print(sum(light for row in lights for light in row))
