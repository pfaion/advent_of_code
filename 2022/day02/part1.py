from itertools import starmap
from pathlib import Path

here = Path(__file__).parent

data = [line.split(" ") for line in (here / "input.txt").read_text().splitlines()]


def score(opponent_move: str, own_move: str) -> int:
    game_score = {
        ("A", "Z"): 0,
        ("B", "X"): 0,
        ("C", "Y"): 0,
        ("A", "X"): 3,
        ("B", "Y"): 3,
        ("C", "Z"): 3,
        ("A", "Y"): 6,
        ("B", "Z"): 6,
        ("C", "X"): 6,
    }[(opponent_move, own_move)]

    move_value = {"X": 1, "Y": 2, "Z": 3}[own_move]

    return game_score + move_value


print(sum(starmap(score, data)))
