from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()


def find_wrong_item(items: str) -> str:
    mid = len(items) // 2
    first_compartment = items[:mid]
    second_compartment = items[mid:]
    overlapping_items = set(first_compartment) & set(second_compartment)
    return next(iter(overlapping_items))


def item_priority(item: str) -> int:
    code = ord(item)
    # capitals come before lowercase in ascii codes
    if code <= ord("Z"):
        return code - ord("A") + 27
    else:
        return code - ord("a") + 1


print(sum(item_priority(find_wrong_item(items)) for items in data))
