from itertools import pairwise
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

result = 0
for line in data_raw:
    nums = [int(val) for val in line.split()][::-1]
    stack = [nums]
    while not all(val == 0 for val in stack[0]):
        diffs = [b - a for a, b in pairwise(stack[0])]
        stack.insert(0, diffs)
    stack[0].append(0)
    for diffs, vals in pairwise(stack):
        vals.append(vals[-1] + diffs[-1])
    result += stack[-1][-1]
print(result)
