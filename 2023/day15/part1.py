from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().strip()


def compute_hash(string: str) -> int:
    value = 0
    for character in string:
        value += ord(character)
        value *= 17
        value = value % 256
    return value


assert compute_hash("HASH") == 52
assert compute_hash("rn=1") == 30

initialization_sequence = data_raw.split(",")
print(sum(compute_hash(step) for step in initialization_sequence))
