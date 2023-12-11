from itertools import pairwise
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text()

W = data.find("\n") + 1
N = data.count("#")
print(*(sum(
    [(b - a - 1) * s + 1, 0][a == b] * i * (N - i)
    for d in map(sorted, zip(*((i // W, i % W) for i, v in enumerate(data) if v == "#")))
    for i, (a, b) in enumerate(pairwise(d), 1)
) for s in (2, 1000000)))
