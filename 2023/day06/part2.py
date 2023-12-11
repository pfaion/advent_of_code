import re
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

time, max_distance = (int("".join(re.findall(r"\d+", line))) for line in data_raw)

print(
    sum(
        1
        for hold_time in range(0, time + 1)
        if (time - hold_time) * hold_time > max_distance
    )
)
