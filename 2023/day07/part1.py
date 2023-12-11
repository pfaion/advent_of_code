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
