import re
from pathlib import Path

strings = Path(__file__).with_name("input.txt").read_text().splitlines()


def is_nice(string: str) -> bool:
    if re.search(r"([aeiou].*){3}", string) is None:
        return False
    if re.search(r"(\w)\1", string) is None:
        return False
    if re.search(r"ab|cd|pq|xy", string) is not None:
        return False
    return True


print(len([string for string in strings if is_nice(string)]))
