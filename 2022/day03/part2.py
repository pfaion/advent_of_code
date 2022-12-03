import re
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text()

batches = [
    match[0] for match in re.finditer(r"\w+\n\w+\n\w+(\n|$)", data_raw, re.MULTILINE)
]


def find_badge(batch: str) -> str:
    elf_items = batch.splitlines()
    overlap = set.intersection(*(set(items) for items in elf_items))
    return next(iter(overlap))


def item_priority(item: str) -> int:
    code = ord(item)
    # capitals come before lowercase in ascii codes
    if code <= ord("Z"):
        return code - ord("A") + 27
    else:
        return code - ord("a") + 1


print(sum(item_priority(find_badge(batch)) for batch in batches))
