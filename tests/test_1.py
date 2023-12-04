from pathlib import Path

import pytest
from aoc2023 import day_1


def test_parse_input_returns_list_of_strings():
    print(Path().absolute())
    given_path = Path("test_input/test_input_1_1.txt")

    parsed_input = day_1.parse_input(given_path)

    assert isinstance(parsed_input, list)
    assert len(parsed_input)
    assert all(isinstance(value, str) for value in parsed_input)


@pytest.mark.parametrize(
    "given_code, expected_value",
    (("1abc2", 12), ("pqr3stu8vwx", 38), ("a1b2c3d4e5f", 15), ("treb7uchet", 77)),
)
def test_decode_calibration_gives_expected_values(given_code, expected_value):
    assert day_1.decode_calibration(given_code) == expected_value


@pytest.mark.parametrize(
    "given_code, expected_value",
    (
        ("two1nine", 29),
        ("eightwothree", 83),
        ("abcone2threexyz", 13),
        ("xtwone3four", 24),
        ("4nineeightseven2", 42),
        ("zoneight234", 14),
        ("7pqrstsixteen", 76),
        ("two934seven1", 21),
        ("59onefourxnmptgtcone", 51),
        ("fourcdqc7vvqhpgqlkjsevenfivefiveseven", 47),
        ("24kmxnlpqxgpsevenfoursixfour", 24),
    ),
)
def test_decode_calibration_handles_spelled_out_numbers(given_code, expected_value):
    assert day_1.decode_calibration(given_code, allow_words=True) == expected_value


@pytest.mark.parametrize(
    "given_code, expected_value",
    (
        ("seven3lbcvjxqhhdpzkttqsixjzzjjbclfq1fiveeightwojx", 72),
        ("oneight", 18),
        ("twone", 21),
        ("threeight", 38),
        ("fiveight", 58),
        ("sevenine", 79),
        ("eightwo", 82),
        ("eighthree", 83),
        ("nineight", 98),
    ),
)
def test_decode_calibration_handles_overlapping_numbers(given_code, expected_value):
    assert day_1.decode_calibration(given_code, allow_words=True) == expected_value


@pytest.mark.parametrize(
    "given_code, expected_value",
    (
        ("38sevennineninemnfzklttkxnine3", 33),
        ("onetwo3two", 12),
    ),
)
def test_decode_row_handles_multiple_instances_of_same_number(
    given_code, expected_value
):
    assert day_1.decode_calibration(given_code, allow_words=True) == expected_value


def test_solving_part_1_gives_expected_value():
    given_input_path = Path("test_input/test_input_1_1.txt")
    answer = day_1.solve_part_one(given_input_path)
    expected_answer = 142
    assert answer == expected_answer


def test_solving_part_2_gives_expected_value():
    given_input_path = Path("test_input/test_input_1_2.txt")
    answer = day_1.solve_part_two(given_input_path)
    expected_answer = 281
    assert answer == expected_answer
