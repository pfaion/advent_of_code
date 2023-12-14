from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

height = len(data_raw)
columns = list(zip(*data_raw))
total_load = 0
for column in columns:
    n_free_above = 0
    for i, cell in enumerate(column):
        if cell == "O":
            final_position = i - n_free_above
            load = height - final_position
            total_load += load
        elif cell == ".":
            n_free_above += 1
        elif cell == "#":
            n_free_above = 0
print(total_load)
