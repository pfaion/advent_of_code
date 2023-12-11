import re
from math import ceil, floor, sqrt
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

time, max_distance = (int("".join(re.findall(r"\d+", line))) for line in data_raw)

# max_distance = (time - hold_time) * hold_time
# m = (t - x) * x
# x^2 - t*x + m = 0
# x = (t +- sqrt(t^2 + 4m) / 2
a = ceil((time - sqrt(time**2 - 4 * max_distance)) / 2)
b = floor((time + sqrt(time**2 - 4 * max_distance)) / 2)
print(b + 1 - a)
