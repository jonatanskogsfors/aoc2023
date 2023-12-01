from pathlib import Path

import pytest

import day_1


def test_parse_input_returns_list_of_strings():
    print(Path().absolute())
    given_path = Path("1/test_input_1.txt")

    parsed_input = day_1.parse_input(given_path)

    assert isinstance(parsed_input, list)
    assert len(parsed_input)
    assert all(isinstance(value, str) for value in parsed_input)


@pytest.mark.parametrize(
    "given_code, expected_number",
    (
        ("1abc2", 12),
        ("pqr3stu8vwx", 38),
        ("a1b2c3d4e5f", 15),
        ("treb7uchet", 77)
    )
)
def test_decode_row_gives_expected_values(given_code, expected_number):
    assert day_1.decode_row(given_code) == expected_number


@pytest.mark.parametrize(
    "given_code, expected_number", 
    (
        ("two1nine", 29),
        ("eightwothree", 83),
        ("abcone2threexyz", 13),
        ("xtwone3four", 24),
        ("4nineeightseven2", 42),
        ("zoneight234", 14),
        ("7pqrstsixteen", 76),
        ("two934seven1", 21),
    )
)
def test_decode_row_handles_spelled_out_numbers(given_code, expected_number):
    assert day_1.decode_row(given_code) == expected_number


@pytest.mark.parametrize(
    "given_code, expected_number", 
    (
        ("seven3lbcvjxqhhdpzkttqsixjzzjjbclfq1fiveeightwojx", 72),
    )
)
def test_decode_row_handles_overlapping_numbers(given_code, expected_number):
    assert day_1.decode_row(given_code) == expected_number


def test_solving_part_1_gives_expected_value():
    given_input_path = Path("1/test_input_1.txt")
    answer = day_1.solve_part_one(given_input_path)
    assert answer == 142


def test_solving_part_2_gives_expected_value():
    given_input_path = Path("1/test_input_2.txt")
    answer = day_1.solve_part_two(given_input_path)
    assert answer == 281
