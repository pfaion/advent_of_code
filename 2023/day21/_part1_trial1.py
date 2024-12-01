from itertools import product
from pathlib import Path

from rich import print
from tqdm import tqdm

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()
width = len(data_raw[0]) + 2
height = len(data_raw) + 2
data = ("#" * width) + "".join("#" + line + "#" for line in data_raw) + ("#" * width)
N = width * height

fields = [i for i, cell in enumerate(data) if i != "#"]

type Coords = tuple[int, int]


def i2coords(i: int) -> Coords:
    row = i // width
    col = i % width
    return row, col


def coords2i(c: Coords) -> int:
    row, col = c
    return width * row + col


def get_neightbors_i(i: int) -> list[int]:
    row, col = i2coords(i)
    return [coords2i((row + dr, col + dc)) for dr, dc in product((-1, 1), (-1, 1))]


inf = float("inf")

# floyd-warshall?
distances = {}
for i in range(N):
    if data[i] == "#":
        continue
    distances[(i, i)] = 0
    for j in get_neightbors_i(i):
        neighbor = data[j]
        if neighbor != "#":
            distances[(i, j)] = 1

for k, i, j in tqdm(product(fields, repeat=3), total=len(fields) ** 3):
    known = distances.get((i, k), inf) + distances.get((k, j), inf)
    if known != inf and distances.get((i, j), inf) > known:
        distances[(i, j)] = known

print(distances)
