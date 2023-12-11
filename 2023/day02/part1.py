from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

max_values = {"red": 12, "green": 13, "blue": 14}

id_sum = 0
for line in data_raw:
    prefix, sets_raw = line.split(":")
    game_id = int(prefix[5:])
    for set_raw in sets_raw.split(";"):
        for entry_raw in set_raw.split(","):
            count_str, color = entry_raw.strip().split(" ")
            count = int(count_str)
            if count > max_values.get(color, 0):
                break
        else:
            continue
        break
    else:
        id_sum += game_id

print(id_sum)
