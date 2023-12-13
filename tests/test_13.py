from pathlib import Path

import pytest
from aoc2023 import day_13
from aoc2023.day_13 import Axis

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_13_1.txt"
TEST_INPUT_2 = TEST_INPUT_DIR / "test_input_13_2.txt"


def test_parse_input_returns_tuple_of_tuple_of_strings():
    patterns = day_13.parse_input(TEST_INPUT_1)
    expected_patterns = 2
    assert len(patterns) == expected_patterns
    assert isinstance(patterns, tuple)
    assert all(isinstance(pattern, tuple) for pattern in patterns)
    assert all(isinstance(row, str) for pattern in patterns for row in pattern)


@pytest.mark.parametrize(
    "given_row, expected_value",
    (
        ("........", 0),
        (".......#", 1),
        ("...#", 1),
        ("#.......", 128),
        ("#...", 8),
        ("#.#.#.", 42),
        ("########", 255),
    ),
)
def test_row_as_number_returns_expected_value(given_row, expected_value):
    value = day_13.row_as_number(given_row)
    assert value == expected_value


@pytest.mark.parametrize(
    "given_input_path, given_pattern_index, expected_axis, expected_length",
    (
        (TEST_INPUT_1, 0, Axis.VERTICAL, 5),
        (TEST_INPUT_1, 1, Axis.HORIZONTAL, 4),
        (TEST_INPUT_2, 0, Axis.VERTICAL, 11),
        (TEST_INPUT_2, 1, Axis.VERTICAL, 1),
    ),
)
def test_find_mirror_in_pattern(
    given_input_path, given_pattern_index, expected_axis, expected_length
):
    pattern = day_13.parse_input(given_input_path)[given_pattern_index]
    mirror_axis, length = day_13.find_mirror(pattern)

    assert mirror_axis == expected_axis
    assert length == expected_length


@pytest.mark.parametrize(
    "given_a, given_b, given_fix_smudges, expected_equality, expected_fixed",
    (
        (1, 1, False, True, False),  # "..#" == "..#"
        (1, 1, True, True, False),  # "..#" == "..#"
        (1, 2, False, False, False),  # "..#" != ".#."
        (1, 2, True, False, False),  # "..#" != ".#."
        (1, 3, False, False, False),  # "..#" != ".##"
        (1, 3, True, True, True),  # "..#" == ".##"
        (1, 65537, False, False, False),  # "..#" != "#..............#"
        (1, 65537, True, True, True),  # "..#" == "#..............#"
    ),
)
def test_rows_are_equal(
    given_a, given_b, given_fix_smudges, expected_equality, expected_fixed
):
    equality, fixed = day_13.rows_are_equal(
        given_a, given_b, fix_smudges=given_fix_smudges
    )
    assert equality == expected_equality
    assert fixed == expected_fixed


@pytest.mark.parametrize(
    "given_input_path, given_pattern_index, expected_axis, expected_length",
    (
        (TEST_INPUT_1, 0, Axis.HORIZONTAL, 3),
        (TEST_INPUT_1, 1, Axis.HORIZONTAL, 1),
    ),
)
def test_find_mirror_in_pattern_with_smudge_fixing(
    given_input_path, given_pattern_index, expected_axis, expected_length
):
    pattern = day_13.parse_input(given_input_path)[given_pattern_index]
    mirror_axis, length = day_13.find_mirror(pattern, fix_smudges=True)

    assert mirror_axis == expected_axis
    assert length == expected_length


def test_solving_part_one_gives_expected_value():
    answer = day_13.solve_part_one(TEST_INPUT_1)
    expected_answer = 405
    assert answer == expected_answer


def test_solving_part_two_gives_expected_value():
    answer = day_13.solve_part_two(TEST_INPUT_1)
    expected_answer = 400
    assert answer == expected_answer
