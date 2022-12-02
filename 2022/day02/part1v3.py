from pathlib import Path

data = (Path(__file__).parent / "input.txt").read_text().splitlines()

print(
    sum(
        1
        + (b := ord((p := l.split(" "))[1]) - 88)
        + 3 * ((b + 4 - (ord(p[0]) - 65)) % 3)
        for l in data
    )
)
