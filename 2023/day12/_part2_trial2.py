import re
from functools import cache
from itertools import takewhile
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

conditions, groups_raw = zip(*(line.split() for line in data_raw))
all_groups = [tuple(line.split(",")) for line in groups_raw]


@cache
def get_pattern(groups: tuple[str]) -> re.Pattern:
    return re.compile(
        r"^[\.\?]*"
        + r"[\.\?]+".join(r"[#\?]{" + n + r"}" for n in groups)
        + r"[\.\?]*$"
    )


@cache
def possible_assignments(condition: str, groups: tuple[str]) -> int:
    if not get_pattern(groups).match(condition):
        return 0
    if "?" not in condition or not groups:
        return 1

    result = 0
    for branch in [condition.replace("?", v, 1) for v in (".", "#")]:
        group_copy = list(groups)
        branch = branch.lstrip(".")
        leading_hash = len(list(takewhile("#".count, branch)))
        if leading_hash == group_copy[0]:
            branch = branch[leading_hash]
            group_copy.pop(0)
        result += possible_assignments(branch, tuple(group_copy))

    return result


repeat = 5
result = 0
for condition, groups in zip(conditions, all_groups):
    condition = "?".join(condition for _ in range(repeat))
    groups = groups * repeat
    line_result = possible_assignments(condition, groups)
    result += line_result
    print(line_result)

print(result)
