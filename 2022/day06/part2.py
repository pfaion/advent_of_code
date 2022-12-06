from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().strip()

for end in range(14, len(data)):
    chunk = data[end - 14 : end]
    if len(set(chunk)) == 14:
        print(end)
        break
