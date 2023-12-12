from pathlib import Path

import pytest
from aoc2023 import day_12

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_12_1.txt"


@pytest.mark.parametrize(
    "given_group, given_substring, expected_match",
    (
        ("###.", "?###", False),
        ("###.", "###?", True),
    ),
)
def test_matches(given_group, given_substring, expected_match):
    match = day_12.matches(given_group, given_substring)
    assert match == expected_match


@pytest.mark.parametrize(
    "given_row, given_groups, expected_arrangements",
    (
        ("??", (1,), 2),
        ("???.###", (1, 1, 3), 1),
    ),
)
def test_arrangements_for_row_short_cases(given_row, given_groups, expected_arrangements):
    arrangements = day_12.arrangements_for_row(given_row, given_groups)
    assert arrangements == expected_arrangements


@pytest.mark.parametrize(
    "given_row, given_groups, expected_arrangements",
    (
        ("???.###", (1, 1, 3), 1),
        (".??..??...?##.", (1, 1, 3), 4),
    ),
)
def test_arrangements_for_row_finds_all_posibilities(
    given_row, given_groups, expected_arrangements
):
    arrangements = day_12.arrangements_for_row(given_row, given_groups)

    assert arrangements == expected_arrangements


def test_parse_input_returns_tuple_of_row_and_groups():
    parsed_input = day_12.parse_input(TEST_INPUT_1)

    expected_records = 6
    assert len(parsed_input) == expected_records

    expected_parts_in_record = 2
    assert all(len(record) == expected_parts_in_record for record in parsed_input)

    assert all(isinstance(record[0], str) for record in parsed_input)
    assert all(isinstance(record[1], tuple) for record in parsed_input)
    assert all(isinstance(group, int) for record in parsed_input for group in record[1])


@pytest.mark.parametrize(
    "given_row, given_groups, expected_row, expected_groups",
    (
        (".#", (1,), ".#?.#?.#?.#?.#", (1, 1, 1, 1, 1)),
        (
            "???.###",
            (1, 1, 3),
            "???.###????.###????.###????.###????.###",
            (1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3),
        ),
    ),
)
def test_unfold_record_returns_fivefold_unfold(
    given_row, given_groups, expected_row, expected_groups
):
    unfolded_row, unfolded_groups = day_12.unfold_record(given_row, given_groups)

    assert len(unfolded_row) == len(given_row) * 5 + 4
    assert len(unfolded_groups) == len(given_groups) * 5

    assert unfolded_row == expected_row
    assert unfolded_groups == expected_groups


def test_solving_part_one_gives_expected_value():
    answer = day_12.solve_part_one(TEST_INPUT_1)
    expected_answer = 21
    assert answer == expected_answer


def test_solving_part_two_gives_expected_value():
    answer = day_12.solve_part_two(TEST_INPUT_1)
    expected_answer = 525152
    assert answer == expected_answer
