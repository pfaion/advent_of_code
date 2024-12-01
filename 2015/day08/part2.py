import json
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

print(sum(len(json.dumps(line)) - len(line) for line in data_raw))
