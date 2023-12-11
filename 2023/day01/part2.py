import re
from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()

digits = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def parse_first_digit(line: str) -> int:
    digit_regex = r"\d|" + r"|".join(digits.keys())
    match = re.search(digit_regex, line)
    value: str = match[0]
    if value.isdigit():
        return int(value)
    return digits[value]


def parse_last_digit(line: str) -> int:
    digit_regex = r"\d|" + r"|".join(word[::-1] for word in digits.keys())
    match = re.search(digit_regex, line[::-1])
    value: str = match[0]
    if value.isdigit():
        return int(value)
    return digits[value[::-1]]


def calibration_value(line: str) -> int:
    first = parse_first_digit(line)
    last = parse_last_digit(line)
    value = first * 10 + last
    return value


print(sum(calibration_value(line) for line in data))
