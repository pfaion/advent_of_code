import re
from functools import cache
from itertools import takewhile
from pathlib import Path

# from rich import print


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


c = {}


def possible_assignments(condition: str, groups: tuple[str], indent=0) -> int:
    prefix = " " * indent
    key = (condition, groups)
    if key in c:
        # print(prefix, condition, groups, f"({c[key]})")
        return c[key]
    if not condition:
        r = 1 if not groups else 0
        # print(prefix, condition, groups, r)
        c[key] = r
        return r
    if not get_pattern(groups).match(condition):
        # print(prefix, condition, groups, 0)
        c[key] = 0
        return 0
    if "?" not in condition or not groups:
        # print(prefix, condition, groups, 1)
        c[key] = 1
        return 1

    # print(prefix, condition, groups, "...")
    result = 0
    for branch in [condition.replace("?", v, 1) for v in (".", "#")]:
        group_copy = list(groups)
        while True:
            if branch.startswith("."):
                branch = branch.lstrip(".")
            elif group_copy and int(group_copy[0]) == (
                leading_hash := len(list(takewhile("#".count, branch)))
            ):
                # need to cut off one more, to ensure that group will be separated from next
                branch = branch[leading_hash + 1 :]
                group_copy.pop(0)
            else:
                break
        result += possible_assignments(branch, tuple(group_copy), indent + 1)

    # print(prefix, f"[{condition}", f"{groups}]", result)
    c[key] = result
    return result


repeat = 5
result = 0
for i, (condition, groups) in enumerate(zip(conditions, all_groups)):
    c = {}
    condition = "?".join(condition for _ in range(repeat))
    groups = groups * repeat
    line_result = possible_assignments(condition, groups)
    result += line_result
    print(i, line_result)

print(result)
