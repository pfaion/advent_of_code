import re
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

times, distances = ([int(val) for val in re.findall(r"\d+", line)] for line in data_raw)
result = 1
for time, max_distance in zip(times, distances):
    n_ways_beating = 0
    for hold_time in range(0, time + 1):
        race_time = time - hold_time
        max_speed = hold_time
        distance = race_time * max_speed
        if distance > max_distance:
            n_ways_beating += 1
    result *= n_ways_beating
print(result)
