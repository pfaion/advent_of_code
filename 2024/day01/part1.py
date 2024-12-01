from pathlib import Path

# read in data
data_raw = Path(__file__).with_name("input.txt").read_text().strip()

# parse data
numbers_1: list[int] = []
numbers_2: list[int] = []
for line in data_raw.splitlines():
    n1, n2 = map(int, line.split())
    numbers_1.append(n1)
    numbers_2.append(n2)

# sort the lists, so we can match the numbers
numbers_1.sort()
numbers_2.sort()

# compute distances
distances = [abs(n1 - n2) for n1, n2 in zip(numbers_1, numbers_2)]

# print total distance
total_distance = sum(distances)
print(total_distance)
