import re
from pathlib import Path

CARD_PATTERN = re.compile(r"Card\s+(\d+):((?:\s+\d+)+)\s+\|((?:\s+\d+)+)")


def main():
    input_path = Path("input/input_4.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))  # 184798


def correct_numbers_for_card(winning_numbers: set, your_numbers: set):
    return len(winning_numbers & your_numbers)


def points_for_card(winning_numbers: set, your_numbers: set):
    correct_numbers = correct_numbers_for_card(winning_numbers, your_numbers)
    return 2 ** (correct_numbers - 1) if correct_numbers else 0


def solve_part_one(input_path):
    cards = parse_input(input_path)
    return sum(
        (
            points_for_card(winning_numbers, your_numbers)
            for winning_numbers, your_numbers in cards.values()
        )
    )


def solve_part_two(input_path):
    cards = parse_input(input_path)
    card_inventory = {card_id: 1 for card_id in cards}
    for card_id in card_inventory:
        card_inventory = scratch_card(card_inventory, cards, card_id)
    return sum(card_inventory.values())


def parse_input(input_path: Path):
    cards = {}
    for card_match in CARD_PATTERN.finditer(input_path.read_text()):
        card_number = int(card_match.group(1))
        winning_numbers = card_match.group(2)
        winning_numbers = set(
            map(int, winning_numbers.strip().replace("  ", " ").split(" "))
        )
        your_numbers = card_match.group(3)
        your_numbers = set(map(int, your_numbers.strip().replace("  ", " ").split(" ")))
        cards[card_number] = (winning_numbers, your_numbers)
    return cards


def scratch_card(card_inventory, cards, card_id):
    correct_numbers = correct_numbers_for_card(*cards[card_id])
    number_of_cards = card_inventory[card_id]
    for n in range(1, correct_numbers + 1):
        new_card = card_id + n
        if new_card not in card_inventory:
            card_inventory[new_card] = 0
        card_inventory[new_card] += number_of_cards
    return card_inventory


if __name__ == "__main__":
    main()
