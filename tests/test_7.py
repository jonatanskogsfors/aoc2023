from pathlib import Path

import pytest
from aoc2023 import day_7
from aoc2023.day_7 import CamelPoker

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_7_1.txt"


@pytest.mark.parametrize(
    "given_hand, expected_type",
    (
        ("AAAAA", CamelPoker.FIVE_OF_A_KIND),
        ("AA8AA", CamelPoker.FOUR_OF_A_KIND),
        ("23332", CamelPoker.FULL_HOUSE),
        ("TTT98", CamelPoker.THREE_OF_A_KIND),
        ("23432", CamelPoker.TWO_PAIRS),
        ("A23A4", CamelPoker.ONE_PAIR),
        ("23456", CamelPoker.HIGH_CARD),
    ),
)
def test_identify_hand(given_hand, expected_type):
    type = day_7.identify_hand(given_hand)
    assert type == expected_type


@pytest.mark.parametrize(
    "given_hands, expected_ranked_hands",
    (
        ((("33233", 0), ("22222", 0)), (("22222", 0), ("33233", 0))),
        (
            (("23456", 0), ("78787", 0), ("9AKAK", 0)),
            (("78787", 0), ("9AKAK", 0), ("23456", 0)),
        ),
        (
            (("KKQQJ", 0), ("QJJAQ", 0), ("A2233", 0)),
            (("A2233", 0), ("KKQQJ", 0), ("QJJAQ", 0)),
        ),
    ),
)
def test_rank_hands(given_hands, expected_ranked_hands):
    ranked_hands = day_7.rank_hands(given_hands)
    assert ranked_hands == expected_ranked_hands


@pytest.mark.parametrize(
    "given_hand, expected_numeric",
    (
        ("23456", (2, 3, 4, 5, 6)),
        ("98787", (9, 8, 7, 8, 7)),
        ("TJQKA", (10, 11, 12, 13, 14)),
    ),
)
def test_numeric_hand_converts_hand_to_numbers(given_hand, expected_numeric):
    numeric = day_7.numeric_hand(given_hand)
    assert numeric == expected_numeric


def test_parse_input_returns_tuples_of_hands_and_bid():
    hands = day_7.parse_input(TEST_INPUT_1)

    expected_number_of_hands = 5
    assert len(hands) == expected_number_of_hands

    assert all(isinstance(hand, str) for hand, _ in hands)
    assert all(isinstance(bid, int) for _, bid in hands)


def test_solving_part_one_gives_expected_value():
    answer = day_7.solve_part_one(TEST_INPUT_1)
    expected_answer = 6440
    assert answer == expected_answer
