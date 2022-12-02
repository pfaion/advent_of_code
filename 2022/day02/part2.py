from itertools import starmap
from pathlib import Path

here = Path(__file__).parent

data = [line.split(" ") for line in (here / "input.txt").read_text().splitlines()]


def score(opponent_move: str, outcome: str) -> int:
    own_move = {
        ("A", "X"): "C",
        ("A", "Y"): "A",
        ("A", "Z"): "B",
        ("B", "X"): "A",
        ("B", "Y"): "B",
        ("B", "Z"): "C",
        ("C", "X"): "B",
        ("C", "Y"): "C",
        ("C", "Z"): "A",
    }[(opponent_move, outcome)]

    game_score = {"X": 0, "Y": 3, "Z": 6}[outcome]
    move_value = {"A": 1, "B": 2, "C": 3}[own_move]

    return game_score + move_value


print(sum(starmap(score, data)))
