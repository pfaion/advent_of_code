from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

# I'm sorry.
print(
    sum(
        2 ** (n_winning - 1)
        for line in data_raw
        if (
            n_winning := len(
                set.intersection(
                    *map(lambda s: set(s.split()), line.split(": ")[1].split(" | "))
                )
            )
        )
        > 0
    )
)
