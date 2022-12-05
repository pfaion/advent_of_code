import re
from itertools import islice
from pathlib import Path
from typing import Iterable


def batched(iterable: Iterable, n: int) -> Iterable[list]:
    it = iter(iterable)
    while batch := list(islice(it, n)):
        yield batch


stacks_raw, moves_raw = Path(__file__).with_name("input.txt").read_text().split("\n\n")

# initialize a list of empty stacks
stacks: list[list] = []
n_stacks = stacks_raw.find("\n") // 4 + 1
for _ in range(n_stacks):
    stacks.append([])

# parse stack data
for line in stacks_raw.splitlines()[:-1]:
    for stack_idx, batch in enumerate(batched(line, 4)):
        item = batch[1]
        if item != " ":
            stacks[stack_idx].insert(0, item)

# process move data
for line in moves_raw.splitlines():
    match = re.match(r"move (\d+) from (\d+) to (\d+)", line)
    n_move, source, target = map(int, match.groups())
    dummy = []
    for _ in range(n_move):
        dummy.append(stacks[source - 1].pop())
    for _ in range(n_move):
        stacks[target - 1].append(dummy.pop())


print("".join(stack[-1] for stack in stacks))
