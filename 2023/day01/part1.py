from pathlib import Path

data = Path(__file__).with_name("input.txt").read_text().splitlines()


def calibration_value(line: str) -> int:
    first = next(char for char in line if char.isdigit())
    last = next(char for char in reversed(line) if char.isdigit())
    value = int(first + last)
    return value


print(sum(calibration_value(line) for line in data))
