from math import prod
from pathlib import Path

here = Path(__file__).parent
data = (here / "input.txt").read_text().splitlines()
dimensions: list[tuple[int, int, int]] = [
    tuple(int(d) for d in line.split("x")) for line in data
]


def required_ribbon(sides: tuple[int, int, int]) -> int:
    smaller_sides = sorted(sides)[0:2]
    return 2 * sum(smaller_sides) + prod(sides)


print(sum(map(required_ribbon, dimensions)))
