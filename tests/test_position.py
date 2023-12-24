import pytest
from aoc2023.position import Position


@pytest.mark.parametrize(
    "given_position_1, given_position_2, expected_manhattan_distance",
    (
        (Position(0, 0), Position(0, 0), 0),
        (Position(3, 0), Position(0, 0), 3),
        (Position(-5, 0), Position(0, 7), 12),
        (Position(3, 5), Position(7, 11), 10),
    ),
)
def test_manhattan_distance(
    given_position_1, given_position_2, expected_manhattan_distance
):
    manhattan_distance = given_position_1.manhattan(given_position_2)
    assert manhattan_distance == expected_manhattan_distance


@pytest.mark.parametrize(
    "given_a, given_b, expected_sum",
    (
        (Position(0, 0), Position(0, 0), Position(0, 0)),
        (Position(1, 3), Position(5, 7), Position(6, 10)),
        (Position(1, 1), Position(-3, -5), Position(-2, -4)),
    ),
)
def test_addition(given_a, given_b, expected_sum):
    position_sum = given_a + given_b
    assert position_sum == expected_sum


@pytest.mark.parametrize(
    "given_a, given_b, expected_difference",
    (
        (Position(0, 0), Position(0, 0), Position(0, 0)),
        (Position(9, 11), Position(3, 7), Position(6, 4)),
        (Position(3, 5), Position(4, 8), Position(-1, -3)),
    ),
)
def test_subtraction(given_a, given_b, expected_difference):
    position_difference = given_a - given_b
    assert position_difference == expected_difference


@pytest.mark.parametrize(
    "given_position, given_scalar, expected_product",
    (
        (Position(0, 0), 1, Position(0, 0)),
        (Position(1, 1), 0, Position(0, 0)),
        (Position(3, 5), 2, Position(6, 10)),
        (Position(3, 5), -2, Position(-6, -10)),
        (Position(-3, -5), -2, Position(6, 10)),
        (Position(3, 5), -2, Position(-6, -10)),
    ),
)
def test_scalar_multiplication(given_position, given_scalar, expected_product):
    position_difference = given_position * given_scalar
    assert position_difference == expected_product
