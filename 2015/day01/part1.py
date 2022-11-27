from pathlib import Path

here = Path(__file__).parent


def get_floor(data: str) -> int:
    return sum(1 if char == "(" else -1 for char in data)


# assert get_floor("(())") == 0
# assert get_floor("()()") == 0
# assert get_floor("(((") == 3
# assert get_floor("(()(()(") == 3
# assert get_floor("))(((((") == 3
# assert get_floor("())") == -1
# assert get_floor("))(") == -1
# assert get_floor(")))") == -3
# assert get_floor(")())())") == -3


data = (here / "input.txt").read_text()
print(get_floor(data))
