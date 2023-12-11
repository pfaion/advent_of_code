from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

print(
    sum(
        (rank0 + 1) * bid
        for rank0, (*_, bid) in enumerate(
            sorted(
                (
                    max(map(hand.count, hand)),
                    -len(set(hand)),
                    *map("23456789TJQKA".index, hand),
                    int(str_bid),
                )
                for hand, str_bid in map(str.split, data_raw)
            )
        )
    )
)
