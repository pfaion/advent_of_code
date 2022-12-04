from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()
data_iter = (
    ((int(bound) for bound in range.split("-")) for range in line.split(","))
    for line in data_raw
)

print(
    sum(
        1
        for ((start_1, end_1), (start_2, end_2)) in data_iter
        if (start_1 <= start_2 <= end_2 <= end_1)
        or (start_2 <= start_1 <= end_1 <= end_2)
    )
)
