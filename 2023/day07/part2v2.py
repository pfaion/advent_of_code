from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

print(
    sum(
        (rank0 + 1) * bid
        for rank0, (*_, bid) in enumerate(
            sorted(
                (
                    max(0, 0, *map(hand.count, set(hand) - {"J"})) + hand.count("J"),
                    -(max(1, len(set(hand) - {"J"}))),
                    *map("J23456789TQKA".index, hand),
                    int(str_bid),
                )
                for hand, str_bid in map(str.split, data_raw)
            )
        )
    )
)
