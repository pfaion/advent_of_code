import re
from math import prod
from pathlib import Path
from typing import Callable

data_raw = Path(__file__).with_name("input.txt").read_text()

n_monkeys = len(re.findall(r"Monkey \d+:", data_raw))
items = [
    [int(item) for item in match.group("items").split(", ")]
    for match in re.finditer(r"items: (?P<items>(\d| |,)+)\n", data_raw)
]


def parse_operation(text: str) -> Callable[[int], int]:
    _, operator_string, operand_string = text.split()
    operator = {"*": prod, "+": sum}[operator_string]
    if operand_string == "old":
        return lambda x: operator((x, x))
    else:
        operand = int(operand_string)
        return lambda x: operator((x, operand))


operations = [
    parse_operation(match.group("operation"))
    for match in re.finditer(r"Operation: new = (?P<operation>.*)\n", data_raw)
]
divisibility = [
    int(match.group("val"))
    for match in re.finditer(r"divisible by (?P<val>\d+)\n", data_raw)
]
next_monkey = [
    {True: int(match.group("true")), False: int(match.group("false"))}
    for match in re.finditer(r"If true: \D+(?P<true>\d+)\n\D+(?P<false>\d+)", data_raw)
]
activities = [0 for _ in range(n_monkeys)]


for round in range(10000):
    for monkey_i in range(n_monkeys):
        while len(items[monkey_i]) > 0:
            activities[monkey_i] += 1
            old = items[monkey_i].pop(0)
            new = operations[monkey_i](old)
            # I don't fully understand this, but I guess taking the modulus of
            # the product of all divisors will keep the operations stable across
            # all divisibility checks but keeps the numbers small. This was a
            # hunch that I tested and it worked, without me 100% understanding
            # why.
            new = new % prod(divisibility)
            target = next_monkey[monkey_i][new % divisibility[monkey_i] == 0]
            items[target].append(new)

monkey_business_level = prod(sorted(activities)[-2:])
print(monkey_business_level)
