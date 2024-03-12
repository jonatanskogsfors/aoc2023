from pathlib import Path

import pytest
from aoc2023 import day_21
from aoc2023.position import Position

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_21_1.txt"


@pytest.mark.parametrize(
    "given_map, expected_start_position",
    (
        (("S",), Position(0, 0)),
        ((".S.",), Position(1, 0)),
        ((".", ".", "S"), Position(0, 2)),
        (("...", "...", "..S"), Position(2, 2)),
    ),
)
def test_find_start_position(given_map, expected_start_position):
    start_position = day_21.get_start_position(given_map)
    assert start_position == expected_start_position


@pytest.mark.parametrize(
    "given_position, given_map, expected_positions",
    (
        (
            Position(1, 1),
            ("...", "...", "..."),
            {Position(1, 0), Position(0, 1), Position(2, 1), Position(1, 2)},
        ),
        (
            Position(0, 0),
            ("...", "...", "..."),
            {Position(0, 1), Position(1, 0)},
        ),
        (
            Position(1, 1),
            ("...", "#..", ".#."),
            {Position(1, 0), Position(2, 1)},
        ),
        (
            Position(2, 2),
            ("...", "..#", ".#."),
            set(),
        ),
    ),
)
def test_find_possible_steps(given_position, given_map, expected_positions):
    positions = day_21.get_possible_positions(given_position, given_map)
    assert positions == expected_positions


@pytest.mark.parametrize("given_input_path", (TEST_INPUT_1,))
def test_parse_input(given_input_path):
    parsed_input = day_21.parse_input(given_input_path)
    assert isinstance(parsed_input, tuple)
    assert all(isinstance(row, str) for row in parsed_input)


def test_solving_part_one_gives_expected_value():
    answer = day_21.solve_part_one(TEST_INPUT_1, 6)
    expected_answer = 16
    assert answer == expected_answer
