from itertools import accumulate, takewhile
from pathlib import Path

here = Path(__file__).parent


def first_basement_enter(data: str) -> int:
    floors = accumulate(1 if char == "(" else -1 for char in data)
    floors_before_basement = takewhile(lambda x: x >= 0, floors)
    return len(list(floors_before_basement)) + 1


# assert first_basement_enter(")") == 1
# assert first_basement_enter("()())") == 5


data = (here / "input.txt").read_text()
print(first_basement_enter(data))
