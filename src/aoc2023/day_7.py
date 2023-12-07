from collections import Counter
from enum import IntEnum
from pathlib import Path


def main():
    input_path = Path("input/input_7.txt")
    print(solve_part_one(input_path))


class CamelPoker(IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIRS = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


def parse_input(input_path: Path):
    hands = input_path.read_text().splitlines()
    return tuple([(card, int(bid)) for card, bid in [hand.split() for hand in hands]])


def identify_hand(hand: str) -> CamelPoker:
    match Counter(hand).most_common():
        case [(_, 5)]:
            hand_type = CamelPoker.FIVE_OF_A_KIND
        case [(_, 4), _]:
            hand_type = CamelPoker.FOUR_OF_A_KIND
        case [(_, 3), (_, 2)]:
            hand_type = CamelPoker.FULL_HOUSE
        case [(_, 3), *_]:
            hand_type = CamelPoker.THREE_OF_A_KIND
        case [(_, 2), (_, 2), *_]:
            hand_type = CamelPoker.TWO_PAIRS
        case [(_, 2), *_]:
            hand_type = CamelPoker.ONE_PAIR
        case _:
            hand_type = CamelPoker.HIGH_CARD
    return hand_type


def numeric_hand(hand: str) -> tuple[int]:
    cards = "23456789TJQKA"
    return tuple([cards.index(card) + 2 for card in hand])


def rank_hands(hands):
    return tuple(
        sorted(
            hands, reverse=True, key=lambda h: (identify_hand(h[0]), *numeric_hand(h[0]))
        )
    )


def solve_part_one(input_path):
    hands = parse_input(input_path)
    ranked_hands = rank_hands(hands)
    winnings = [
        bid * rank for rank, (_, bid) in enumerate(reversed(ranked_hands), start=1)
    ]
    return sum(winnings)


if __name__ == "__main__":
    main()
