from pathlib import Path

import pytest
from aoc2023 import day_6

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_6_1.txt"


@pytest.mark.parametrize(
    "given_button_time, expected_distance",
    (
        (0, 0),
        (1, 6),
        (2, 10),
        (3, 12),
        (4, 12),
        (5, 10),
        (6, 6),
        (7, 0),
    ),
)
def test_race_7_ms_calculates_the_expected_times(given_button_time, expected_distance):
    given_race_duration = 7
    distance = day_6.race(given_race_duration, given_button_time)
    assert distance == expected_distance


@pytest.mark.parametrize(
    "given_race_duration, given_record, expected_strategies",
    (
        (7, 9, 4),
        (15, 40, 8),
        (30, 200, 9),
    ),
)
def test_find_record_breakers_returns_the_expected_strategies(
    given_race_duration, given_record, expected_strategies
):
    strategies = day_6.find_record_breakers(given_race_duration, given_record)
    assert len(strategies) == expected_strategies


def test_calculate_number_of_strategies_handles_when_there_are_no_solutions():
    given_race_duration = 10
    given_record = 1337
    number_of_strategies = day_6.calculate_number_of_strategies(
        given_race_duration, given_record
    )

    assert number_of_strategies == 0


@pytest.mark.parametrize(
    "given_race_duration, given_record",
    (
        (7, 9),
        (7, 10),
        (7, 100),
        (15, 40),
        (20, 200),
        (30, 400),
    ),
)
def test_calculate_number_of_strategies_agrees_with_find_record_breakers(
    given_race_duration, given_record
):
    found_strategies = day_6.find_record_breakers(given_race_duration, given_record)
    number_of_strategies = day_6.calculate_number_of_strategies(
        given_race_duration, given_record
    )

    assert len(found_strategies) == number_of_strategies


def test_parse_input_returns_tuples_of_time_and_distance():
    races = day_6.parse_input(TEST_INPUT_1)
    assert races == ((7, 9), (15, 40), (30, 200))


def test_parse_input_with_kerning_returns_time_and_distance():
    race_time, record = day_6.parse_input(TEST_INPUT_1, kern=True)
    expected_race_time = 71530
    expected_record = 940200
    assert race_time == expected_race_time
    assert record == expected_record


def test_solving_part_one_gives_expected_value():
    answer = day_6.solve_part_one(TEST_INPUT_1)
    expected_answer = 288
    assert answer == expected_answer


def test_solving_part_two_gives_expected_value():
    answer = day_6.solve_part_two(TEST_INPUT_1)
    expected_answer = 71503
    assert answer == expected_answer
