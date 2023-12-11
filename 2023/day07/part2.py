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
