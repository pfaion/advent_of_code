import re
from pathlib import Path

strings = Path(__file__).with_name("input.txt").read_text().splitlines()


def is_nice(string: str) -> bool:
    if re.search(r"(\w\w).*\1", string) is None:
        return False
    if re.search(r"(\w).\1", string) is None:
        return False
    return True


print(len([string for string in strings if is_nice(string)]))
