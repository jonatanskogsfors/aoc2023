from pathlib import Path

import pytest
from aoc2023 import day_9

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_9_1.txt"


@pytest.mark.parametrize(
    "given_sequence, expected_derivative",
    (
        ((1, 2, 3, 4), (1, 1, 1)),
        ((1, 2, 4, 8, 16), (1, 2, 4, 8)),
        ((1, 1, 1), (0, 0)),
        ((0, 0, 0, 0, 0), None),
    ),
)
def test_derive_returns_the_expected_sequence(given_sequence, expected_derivative):
    derivative = day_9.derive(given_sequence)
    assert derivative == expected_derivative


@pytest.mark.parametrize(
    "given_sequence, expected_next_number",
    (
        ((0, 3, 6, 9, 12, 15), 18),
        ((1, 3, 6, 10, 15, 21), 28),
        ((10, 13, 16, 21, 30, 45), 68),
    ),
)
def test_next_number_returns_the_expected_value(given_sequence, expected_next_number):
    next_number = day_9.next_number(given_sequence)
    assert next_number == expected_next_number


@pytest.mark.parametrize(
    "given_sequence, expected_next_number",
    (
        ((0, 3, 6, 9, 12, 15), -3),
        ((1, 3, 6, 10, 15, 21), 0),
        ((10, 13, 16, 21, 30, 45), 5),
    ),
)
def test_previous_number_returns_the_expected_value(given_sequence, expected_next_number):
    previous_number = day_9.next_number(given_sequence, left=True)
    assert previous_number == expected_next_number


def test_parse_input_returns_tuple_of_tuple_of_ints():
    # Given an input path
    # When parsing input
    sequences = day_9.parse_input(TEST_INPUT_1)

    # Then the result is not empty
    assert sequences

    # And the result is a tuple
    assert isinstance(sequences, tuple)

    # And each element is a tuple
    assert all(isinstance(sequence, tuple) for sequence in sequences)

    # And the sub-tuples are not empty
    assert all(sequence for sequence in sequences)

    # And the innermost elements are ints
    assert all(isinstance(element, int) for sequence in sequences for element in sequence)


def test_solving_part_one_gives_expected_value():
    answer = day_9.solve_part_one(TEST_INPUT_1)
    expected_answer = 114
    assert answer == expected_answer


def test_solving_part_two_gives_expected_value():
    answer = day_9.solve_part_two(TEST_INPUT_1)
    expected_answer = 2
    assert answer == expected_answer
