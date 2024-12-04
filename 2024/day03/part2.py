import re
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().strip()

pattern = "".join(
    [
        r"do\(\)",
        r"|",
        r"don't\(\)",
        r"|",
        r"mul",
        r"\(",
        r"(?P<a>\d{1,3})",
        r",",
        r"(?P<b>\d{1,3})",
        r"\)",
    ]
)

result = 0
enabled = True
for match in re.finditer(pattern, data, re.MULTILINE):
    string = match.group(0)
    if string == "do()":
        enabled = True
    elif string == "don't()":
        enabled = False
    elif enabled:
        result += int(match.group("a")) * int(match.group("b"))

print(result)
