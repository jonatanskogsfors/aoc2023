from pathlib import Path

import pytest
from aoc2023 import day_18
from aoc2023.direction import Direction
from aoc2023.position import Position

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_18_1.txt"


def test_calculate_needed_space_to_contain_lagoon():
    dig_plan = day_18.parse_input(TEST_INPUT_1)
    bounding_box, _ = day_18.create_bounding_box(dig_plan)
    expected_width = 7
    expected_height = 10
    height = len(bounding_box)
    width = len(bounding_box[0])
    assert width == expected_width
    assert height == expected_height

@pytest.mark.parametrize(
    "given_lagoon, given_position, given_direction, given_length, expected_lagoon, expected_position",
    (
        (("...", "...", "..."), Position(2, 0), Direction.DOWN, 2, ("..#", "..#", "..#"), Position(2, 2)),
    )
)
def test_dig_trench(given_lagoon, given_position, given_direction, given_length, expected_lagoon, expected_position):
    new_lagoon, new_position = day_18.dig_trench(given_lagoon, given_position, given_direction, given_length)
    assert new_lagoon == expected_lagoon
    assert new_position == expected_position


def test_create_outline():
    dig_plan = day_18.parse_input(TEST_INPUT_1)
    outline = day_18.create_outline(dig_plan)
    expected_size = 38
    assert sum(row.count("#") for row in outline) == expected_size

@pytest.mark.parametrize(
    "given_lagoon, given_position, expected_lagoon",
    (
        (
            (".###.", "##.##", "#...#", "#..##", "###."),
            Position(2, 2),
            (".###.", "#####", "#####", "#####", "###."),
        ),
        (
            (".###.", "##.##", "#...#", "#..##", "###."),
            Position(0, 0),
            (".###.", "##.##", "#...#", "#..##", "###."),
        ),
    ),
)
def test_flood_fill(given_lagoon, given_position, expected_lagoon):
    new_lagoon = day_18.flood_fill(given_lagoon, given_position)
    assert new_lagoon == expected_lagoon

@pytest.mark.parametrize(
    "given_color, expected_direction, expected_length",
    (
        ("#70c710", Direction.RIGHT, 461937),
        ("#0dc571", Direction.DOWN, 56407),
        ("#5713f0", Direction.RIGHT, 356671),
        ("#d2c081", Direction.DOWN, 863240),
        ("#59c680", Direction.RIGHT, 367720),
        ("#411b91", Direction.DOWN, 266681),
        ("#8ceee2", Direction.LEFT, 577262),
        ("#caa173", Direction.UP, 829975),
        ("#1b58a2", Direction.LEFT, 112010),
        ("#caa171", Direction.DOWN, 829975),
        ("#7807d2", Direction.LEFT, 491645),
        ("#a77fa3", Direction.UP, 686074),
        ("#015232", Direction.LEFT, 5411),
        ("#7a21e3", Direction.UP, 500254),
    )
)
def test_instruction_from_color(given_color, expected_direction, expected_length):
    direction, length = day_18.instruction_from_color(given_color)
    assert direction == expected_direction
    assert length == expected_length

def test_solving_part_one_gives_expected_value():
    answer = day_18.solve_part_one(TEST_INPUT_1)
    expected_answer = 62
    assert answer == expected_answer


def test_solving_part_two_gives_expected_value():
    answer = day_18.solve_part_one(TEST_INPUT_1)
    expected_answer = 952408144115
    assert answer == expected_answer