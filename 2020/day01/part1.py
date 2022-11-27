from math import prod
from pathlib import Path
from typing import Sequence

here = Path(__file__).parent
data = list(map(int, (here / "input.txt").read_text().splitlines()))


def find_summands(data: Sequence[int], target: int) -> tuple[int, int]:
    for idx, a in enumerate(data):
        for b in data[idx + 1 :]:
            if a + b == target:
                return (a, b)
    raise ValueError("Could not create target sum from data.")


def test_demo_data():
    assert find_summands((1721, 979, 366, 299, 675, 1456), 2020) == (1721, 299)


print(prod(find_summands(data, 2020)))
