from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text()

patterns = data_raw.split("\n\n")


result = 0
for pattern in patterns:
    rows = pattern.splitlines()
    n_rows = len(rows)
    reflected_rows = []
    for rowi, row in enumerate(rows[:-1]):
        if all(
            rows[rowi - offset] == rows[rowi + offset + 1]
            for offset in range(min(rowi + 1, n_rows - rowi - 1))
        ):
            reflected_rows.append(rowi + 1)
    for v in reflected_rows:
        result += v * 100

    cols = ["".join(col) for col in zip(*rows)]
    n_cols = len(cols)
    reflected_cols = []
    for coli, col in enumerate(cols[:-1]):
        if all(
            cols[coli - offset] == cols[coli + offset + 1]
            for offset in range(min(coli + 1, n_cols - coli - 1))
        ):
            reflected_cols.append(coli + 1)

    for v in reflected_cols:
        result += v

print(result)
