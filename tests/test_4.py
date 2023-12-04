from pathlib import Path

import pytest
from aoc2023 import day_4

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_4_1.txt"


@pytest.mark.parametrize(
    "given_winning_numbers, given_your_numbers, expected_points",
    (
        ({41, 48, 83, 86, 17}, {83, 86, 6, 31, 17, 9, 48, 53}, 8),
        ({13, 32, 20, 16, 61}, {61, 30, 68, 82, 17, 32, 24, 19}, 2),
        ({1, 21, 53, 59, 44}, {69, 82, 63, 72, 16, 21, 14, 1}, 2),
        ({41, 92, 73, 84, 69}, {59, 84, 76, 51, 58, 5, 54, 83}, 1),
        ({87, 83, 26, 28, 32}, {88, 30, 70, 12, 93, 22, 82, 36}, 0),
        ({31, 18, 13, 56, 72}, {74, 77, 10, 23, 35, 67, 36, 11}, 0),
    ),
)
def test_point_for_card(given_winning_numbers, given_your_numbers, expected_points):
    assert (
        day_4.points_for_card(given_winning_numbers, given_your_numbers)
        == expected_points
    )


def test_parse_input_returns_dict_of_two_sets_of_numbers():
    parsed_input = day_4.parse_input(TEST_INPUT_1)

    assert parsed_input
    assert isinstance(parsed_input, dict)

    first_card = parsed_input[1]
    assert first_card

    assert first_card[0]
    assert first_card[1]
    assert isinstance(first_card[0], set)
    assert isinstance(first_card[1], set)
    assert all(isinstance(value, int) for value in first_card[0])
    assert all(isinstance(value, int) for value in first_card[1])


def test_winning_gives_more_scratchcards():
    given_cards = day_4.parse_input(TEST_INPUT_1)
    given_card_inventory = {1: 2, 2: 1}
    updated_card_inventory = day_4.scratch_card(given_card_inventory, given_cards, 1)

    expected_card_inventory = {1: 2, 2: 3, 3: 2, 4: 2, 5: 2}
    assert updated_card_inventory == expected_card_inventory


def test_solving_part_one_gives_expected_value():
    answer = day_4.solve_part_one(TEST_INPUT_1)
    expected_answer = 13
    assert answer == expected_answer


def test_solving_part_two_gives_expected_value():
    answer = day_4.solve_part_two(TEST_INPUT_1)
    expected_answer = 30
    assert answer == expected_answer
