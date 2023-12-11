from pathlib import Path

import pytest
from aoc2023 import day_11
from aoc2023.position import Position

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_11_1.txt"


def test_expand_image_moves_stars():
    given_image_data = (
        "#..",
        "...",
        "...",
        "..#",
    )

    given_image = day_11.AstronomicalImage(given_image_data)
    stars_before_expansion = given_image.stars()

    given_image.expand()

    stars = given_image.stars()

    expected_stars = {Position(0, 0), Position(3, 5)}
    assert stars != stars_before_expansion
    assert stars == expected_stars


def test_stars_for_astronomical_images_returns_set_of_stars():
    given_image_data = (
        "#..",
        "..#",
        ".#.",
        "..#",
    )
    given_image = day_11.AstronomicalImage(given_image_data)
    stars = given_image.stars()

    expected_stars = {Position(0, 0), Position(2, 1), Position(1, 2), Position(2, 3)}
    assert stars == expected_stars


def test_solving_part_one_gives_expected_value():
    answer = day_11.solve_part_one(TEST_INPUT_1)
    expected_answer = 374
    assert answer == expected_answer


@pytest.mark.parametrize("given_expansion, expected_answer", ((10, 1030), (100, 8410)))
def test_solving_part_two_gives_expected_value(given_expansion, expected_answer):
    answer = day_11.solve_part_two(TEST_INPUT_1, expansion_factor=given_expansion)
    assert answer == expected_answer
