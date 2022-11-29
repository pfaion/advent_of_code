from itertools import starmap
from pathlib import Path

here = Path(__file__).parent
data: list[tuple[int, int, int]] = [
    map(int, line.split("x")) for line in (here / "input.txt").read_text().splitlines()
]


def required_paper(l: int, w: int, h: int) -> int:
    sides = (l * w, w * h, h * l)
    paper = 2 * sum(sides) + min(sides)
    return paper


print(sum(starmap(required_paper, data)))
