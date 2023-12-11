from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

n_cards = len(data_raw)
card_counts = {i: 1 for i in range(n_cards)}

for i, line in enumerate(data_raw):
    n_winning = len(
        set.intersection(
            *map(lambda s: set(s.split()), line.split(": ")[1].split(" | "))
        )
    )
    current_count = card_counts[i]
    for offset in range(1, n_winning + 1):
        if (duplication_i := i + offset) in card_counts:
            card_counts[duplication_i] += current_count

print(sum(card_counts.values()))
