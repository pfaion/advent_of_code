# Day 7

[Exercise Text](https://adventofcode.com/2023/day/7)

## Part 1
### Overview
| Variant | Runtime | Size |
| --- | --- | --- |
|1|0.032s|1305|
|2|0.024s|510|

### Variant 1
```python
from collections import Counter
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

data = [((parts := line.split())[0], int(parts[1])) for line in data_raw]

card_ranking = "AKQJT98765432"[::-1]
rank_translation_table = {
    ord(card): rank + ord("a") for rank, card in enumerate(card_ranking)
}


def sort_key(hand: str) -> str:
    counts = Counter(hand)
    max_val = max(counts.values())
    patch = hand.translate(rank_translation_table)
    match (max_val, len(counts)):
        case (5, 1):
            # five of a kind
            return "6" + patch
        case (4, 2):
            # four of a kind
            return "5" + patch
        case (3, 2):
            # full house
            return "4" + patch
        case (3, 3):
            # three of a kind
            return "3" + patch
        case (2, 3):
            # two pair
            return "2" + patch
        case (2, 4):
            # one pair
            return "1" + patch
        case (1, 5):
            # high card
            return "0" + patch


print(
    sum(
        # (hand, rank, bid, sort_key(hand), (rank + 1) * bid)
        (rank + 1) * bid
        for rank, (hand, bid) in enumerate(
            sorted(data, key=lambda entry: sort_key(entry[0]))
        )
    )
)

```
Runtime: 0.032s, Size: 1305, Output:
```
253205868
```
### Variant 2
```python
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

```
Runtime: 0.024s, Size: 510, Output:
```
253205868
```
## Part 2
### Overview
| Variant | Runtime | Size |
| --- | --- | --- |
|1|0.024s|1920|
|2|0.023s|566|

### Variant 1
```python
from collections import Counter
from enum import Enum
from pathlib import Path

data_raw = Path(__file__).with_name("input.txt").read_text().splitlines()

data = [((parts := line.split())[0], int(parts[1])) for line in data_raw]

card_ranking = "AKQT98765432J"[::-1]
rank_translation_table = {
    ord(card): rank + ord("a") for rank, card in enumerate(card_ranking)
}


class Group(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


def get_group(hand: str) -> Group:
    counts = Counter(hand)
    max_val = max(counts.values())
    match (max_val, len(counts)):
        case (5, 1):
            return Group.FIVE_OF_A_KIND
        case (4, 2):
            if counts["J"] > 0:
                return Group.FIVE_OF_A_KIND
            return Group.FOUR_OF_A_KIND
        case (3, 2):
            if counts["J"] > 0:
                return Group.FIVE_OF_A_KIND
            return Group.FULL_HOUSE
        case (3, 3):
            if counts["J"] > 0:
                return Group.FOUR_OF_A_KIND
            return Group.THREE_OF_A_KIND
        case (2, 3):
            if counts["J"] == 1:
                return Group.FULL_HOUSE
            if counts["J"] == 2:
                return Group.FOUR_OF_A_KIND
            return Group.TWO_PAIR
        case (2, 4):
            if counts["J"] > 0:
                return Group.THREE_OF_A_KIND
            return Group.ONE_PAIR
        case (1, 5):
            if counts["J"] > 0:
                return Group.ONE_PAIR
            return Group.HIGH_CARD


def sort_key(hand: str) -> list[int]:
    group = get_group(hand)
    ranks = hand.translate(rank_translation_table)
    return str(group.value) + ranks


print(
    sum(
        (rank + 1) * bid
        for rank, (_hand, bid) in enumerate(
            sorted(data, key=lambda entry: sort_key(entry[0]))
        )
    )
)

```
Runtime: 0.024s, Size: 1920, Output:
```
253907829
```
### Variant 2
```python
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

```
Runtime: 0.023s, Size: 566, Output:
```
253907829
```