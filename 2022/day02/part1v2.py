from itertools import starmap
from pathlib import Path

here = Path(__file__).parent

data = [line.split(" ") for line in (here / "input.txt").read_text().splitlines()]


def score(opponent_move: str, own_move: str) -> int:
    # computing the result based on the ascii values of the characters
    a = ord(opponent_move) - ord("A")
    b = ord(own_move) - ord("X")
    return ((b - a + 4) % 3) * 3 + b + 1


print(sum(starmap(score, data)))
