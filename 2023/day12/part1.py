import re
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

conditions, groups_raw = zip(*(line.split() for line in data_raw))
groups = [line.split(",") for line in groups_raw]

result = 0
for condition, group in zip(conditions, groups):
    pattern = re.compile(
        r"^[\.\?]*" + r"[\.\?]+".join(r"[#\?]{" + n + r"}" for n in group) + r"[\.\?]*$"
    )
    stack = [condition]
    line_result = 0
    while stack:
        assignment: str = stack.pop()
        if not pattern.match(assignment):
            continue
        if "?" not in assignment:
            line_result += 1
            continue
        stack.append(re.sub(r"\?", ".", assignment, count=1))
        stack.append(re.sub(r"\?", "#", assignment, count=1))
    result += line_result

print(result)
