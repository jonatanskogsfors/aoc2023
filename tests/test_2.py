from pathlib import Path

import pytest
from aoc2023 import day_2


def test_parse_input_returns_a_dictionary_of_strings():
    given_path = Path("test_input/test_input_2_1.txt")
    parsed_input = day_2.parse_input(given_path)

    assert parsed_input
    assert isinstance(parsed_input, dict)
    assert all(isinstance(key, int) for key in parsed_input)
    assert all(isinstance(value, str) for value in parsed_input.values())


@pytest.mark.parametrize(
    "given_game, expected_status",
    (
        ("3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", True),
        ("1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", True),
        ("8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", False),
        ("1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red", False),
        ("6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", True),
    ),
)
def test_is_game_possible_should_return_the_correct_status(given_game, expected_status):
    given_rule = {"red": 12, "green": 13, "blue": 14}
    assert day_2.is_game_possible(given_game, given_rule) == expected_status


@pytest.mark.parametrize(
    "given_game, expected_fewest",
    (
        (
            "3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
            {"red": 4, "green": 2, "blue": 6},
        ),
        (
            "1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
            {"red": 1, "green": 3, "blue": 4},
        ),
        (
            "8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
            {"red": 20, "green": 13, "blue": 6},
        ),
        (
            "1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
            {"red": 14, "green": 3, "blue": 15},
        ),
        (
            "6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
            {"red": 6, "green": 3, "blue": 2},
        ),
    ),
)
def test_fewest_cubes_for_game_returns_expected_vlue(given_game, expected_fewest):
    assert day_2.max_by_color(given_game) == expected_fewest


def test_solving_part_1_gives_expected_value():
    given_input_path = Path("test_input/test_input_2_1.txt")
    answer = day_2.solve_part_one(given_input_path)
    assert answer == 8


def test_solving_part_2_gives_expected_value():
    given_input_path = Path("test_input/test_input_2_1.txt")
    answer = day_2.solve_part_two(given_input_path)
    assert answer == 2286
