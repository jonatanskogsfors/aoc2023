from pathlib import Path

import pytest
from aoc2023 import day_17
from aoc2023.position import Position

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_17_1.txt"


@pytest.mark.parametrize(
    "given_graph, expected_cost",
    (
        (((9, 1, 5), (9, 2, 8), (8, 2, 3)), 8),
        (((9, 1, 1, 1, 1), (9, 9, 9, 2, 1)), 6),
        (((1, 1, 2, 9, 9, 9), (9, 1, 1, 1, 1, 1)), 7),
        (
            (
                (1, 1, 1, 9, 9),
                (1, 2, 1, 9, 9),
                (9, 9, 1, 9, 9),
                (9, 9, 1, 3, 1),
                (9, 9, 1, 1, 1),
            ),
            9,
        ),
    ),
)
def test_find_shortest_path(given_graph, expected_cost):
    height = len(given_graph)
    width = len(given_graph[0])

    given_start = Position(0, 0)
    given_goal = Position(width - 1, height - 1)
    cost = day_17.dijkstras_algorithm(given_graph, given_start, given_goal)
    assert cost == expected_cost


def test_parse_input_returns_tuple_of_tuple_of_ints():
    parsed_input = day_17.parse_input(TEST_INPUT_1)
    assert parsed_input
    assert isinstance(parsed_input, tuple)
    assert all(row for row in parsed_input)
    assert all(isinstance(row, tuple) for row in parsed_input)
    assert all(isinstance(element, int) for row in parsed_input for element in row)


def test_solving_part_one_gives_expected_value():
    answer = day_17.solve_part_one(TEST_INPUT_1)
    expected_answer = 102
    assert answer == expected_answer


def test_solving_part_two_gives_expected_value():
    answer = day_17.solve_part_two(TEST_INPUT_1)
    expected_answer = "?"
    assert answer == expected_answer
