import functools
import json
import re
from math import prod
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text()


def compare(left, right) -> int:
    """Returns 1 if right order, -1 if wrong order, 0 if undecided"""
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 1
        if left > right:
            return -1
        return 0
    if isinstance(left, list) and isinstance(right, list):
        for l, r in zip(left, right):
            match compare(l, r):
                case -1:
                    return -1
                case 1:
                    return 1
                case 0:
                    continue
        if len(left) < len(right):
            return 1
        if len(left) > len(right):
            return -1
        return 0
    if isinstance(left, int):
        return compare([left], right)
    if isinstance(right, int):
        return compare(left, [right])


packets = [json.loads(line) for line in re.split(r"\n+", data_raw)]
dividers = ([[2]], [[6]])
packets.extend(dividers)
sorted_packets = sorted(packets, key=functools.cmp_to_key(compare), reverse=True)
print(prod(1 + sorted_packets.index(div) for div in dividers))
