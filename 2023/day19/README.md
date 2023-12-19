# Day 19

[Exercise Text](https://adventofcode.com/2023/day/19)

## Part 1
```python
import re
from pathlib import Path

workflows_raw, parts_raw = map(
    str.splitlines, Path(__file__).with_name("input.txt").read_text().split("\n\n")
)

workflows = {}
pattern = re.compile(r"([xmas][<>]\d+):(\w+)")
for line in workflows_raw:
    name = line.split("{")[0]
    code = "lambda x,m,a,s: "
    for check, result in pattern.findall(line):
        code += f"{repr(result)} if {check} else "
    default = line.split(",")[-1][:-1]
    code += repr(default)
    workflows[name] = eval(code)

parts = [eval(f"dict({line[1:-1]})") for line in parts_raw]

result = 0
for part in parts:
    current = "in"
    while current not in "AR":
        current = workflows[current](**part)
    if current == "A":
        result += sum(part.values())

print(result)

```
Runtime: 0.044s, Size: 763, Output:
```
575412
```
## Part 2
```python
import re
from dataclasses import dataclass
from pathlib import Path

workflows_raw = (
    Path(__file__).with_name("input.txt").read_text().split("\n\n")[0].splitlines()
)


@dataclass
class Rule:
    key: str
    op: str
    value: int
    next_accepted: str
    next_rejected: str


rules: dict[str, Rule] = {}
pattern = re.compile(r"([xmas])([<>])(\d+):(\w+)")
for line in workflows_raw:
    workflow = line.split("{")[0]
    n_rules = line.count(",")
    default = line.split(",")[-1][:-1]
    for i, (key, op, value_str, result) in enumerate(pattern.findall(line)):
        rule_name = f"{workflow}_{i}"
        is_last = i == n_rules - 1
        next_accepted = f"{result}_0"
        next_rejected = f"{default}_0" if is_last else f"{workflow}_{i + 1}"
        rules[rule_name] = Rule(key, op, int(value_str), next_accepted, next_rejected)
rules["in"] = rules["in_0"]


type PartRange = dict[str, tuple[int, int]]


def get_accepted_parts(part: PartRange, start: str) -> int:
    if start == "R_0":
        return 0
    if start == "A_0":
        result = 1
        for lower, upper in part.values():
            result *= upper - lower + 1
        return result

    count = 0
    rule = rules[start]
    lower, upper = part[rule.key]

    if rule.op == "<":
        lower_accept = min(lower, rule.value - 1)
        upper_accept = min(upper, rule.value - 1)
        if lower_accept <= upper_accept:
            count += get_accepted_parts(
                {**part, rule.key: (lower_accept, upper_accept)}, rule.next_accepted
            )

        lower_reject = max(lower, rule.value)
        upper_reject = max(upper, rule.value)
        if lower_reject <= upper_reject:
            count += get_accepted_parts(
                {**part, rule.key: (lower_reject, upper_reject)}, rule.next_rejected
            )
    elif rule.op == ">":
        lower_accept = max(lower, rule.value + 1)
        upper_accept = max(upper, rule.value + 1)
        if lower_accept <= upper_accept:
            count += get_accepted_parts(
                {**part, rule.key: (lower_accept, upper_accept)}, rule.next_accepted
            )

        lower_reject = min(lower, rule.value)
        upper_reject = min(upper, rule.value)
        if lower_reject <= upper_reject:
            count += get_accepted_parts(
                {**part, rule.key: (lower_reject, upper_reject)}, rule.next_rejected
            )
    return count


result = get_accepted_parts(
    {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)},
    start="in",
)

print(result)

```
Runtime: 0.032s, Size: 2554, Output:
```
126107942006821
```