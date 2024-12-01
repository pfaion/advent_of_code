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

# compute similarity score
similarity_score = 0
for n1 in numbers_1:
    count = numbers_2.count(n1)
    similarity_score += n1 * count

# print result
print(similarity_score)
