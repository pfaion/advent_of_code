from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()
# padding to avoid bounds checking
width = len(data_raw[0]) + 2
heigth = len(data_raw) + 2
data_raw = ["." * width] + ["." + line + "." for line in data_raw] + ["." * width]

# precompute symbol-adjacent coords, as we have to compute less neighborhoods that way
type Point = tuple[int, int]
symbol_adjacent_coords: set[Point] = set()
for row, line in enumerate(data_raw):
    for col, char in enumerate(line):
        if not char.isdigit() and char != ".":
            symbol_adjacent_coords.update(
                {
                    (row - 1, col - 1),
                    (row - 1, col),
                    (row - 1, col + 1),
                    (row, col - 1),
                    (row, col + 1),
                    (row + 1, col - 1),
                    (row + 1, col),
                    (row + 1, col + 1),
                }
            )

part_number_sum = 0
for row, line in enumerate(data_raw):
    current = ""
    is_adjacent = False
    for col, char in enumerate(line):
        if not char.isdigit() and current != "":
            if is_adjacent:
                part_number_sum += int(current)
            current = ""
            is_adjacent = False
        elif char.isdigit():
            current += char
            if (row, col) in symbol_adjacent_coords:
                is_adjacent = True

print(part_number_sum)
