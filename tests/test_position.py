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
