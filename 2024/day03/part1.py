import re
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().strip()

pattern = "".join(
    [
        r"mul",
        r"\(",
        r"(?P<a>\d{1,3})",
        r",",
        r"(?P<b>\d{1,3})",
        r"\)",
    ]
)
result = sum(
    int(match.group("a")) * int(match.group("b"))
    for match in re.finditer(pattern, data, re.MULTILINE)
)

print(result)
