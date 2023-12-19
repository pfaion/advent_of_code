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
