from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().strip()

for end in range(4, len(data)):
    chunk = data[end - 4 : end]
    if len(set(chunk)) == 4:
        print(end)
        break
