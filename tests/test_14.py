from pathlib import Path

import pytest
from aoc2023 import day_14
from aoc2023.day_14 import Direction

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_14_1.txt"


@pytest.mark.parametrize(
    "given_positions, given_direction, expected_positions",
    (
        (("..", "O."), Direction.NORTH, ("O.", "..")),
        (("O..", ".O.", "O.O", "OO."), Direction.NORTH, ("OOO", "OO.", "O..", "...")),
        (
            ("..#.", ".#..", "#...", "OOOO"),
            Direction.NORTH,
            ("..#O", ".#O.", "#O..", "O..."),
        ),
        (("....", ".O..", "...."), Direction.NORTH, (".O..", "....", "....")),
        (("....", ".O..", "...."), Direction.SOUTH, ("....", "....", ".O..")),
        (("....", ".O..", "...."), Direction.WEST, ("....", "O...", "....")),
        (("....", ".O..", "...."), Direction.EAST, ("....", "...O", "....")),
    ),
)
def test_titling_the_platform_causes_the_stones_to_move(
    given_positions, given_direction, expected_positions
):
    new_positions = day_14.tilt_platform(given_positions, given_direction)
    assert new_positions == expected_positions


@pytest.mark.parametrize(
    "given_positions, given_spin_cycles, expected_positions",
    (
        (("...", ".O.", "..."), 1, ("...", "...", "..O")),
        (("...", "#..", "O.."), 1, ("...", "#..", "..O")),
        (("...", "#..", "O.."), 2, ("..O", "#..", "...")),
    ),
)
def test_spin_cycle_causes_the_stones_to_move(
    given_positions, given_spin_cycles, expected_positions
):
    new_positions = day_14.spin_cycle(given_positions, given_spin_cycles)
    assert new_positions == expected_positions


def test_parse_input_returns_tuple_of_strings():
    parsed_input = day_14.parse_input(TEST_INPUT_1)
    assert parsed_input
    assert all(isinstance(row, str) for row in parsed_input)


@pytest.mark.parametrize(
    "given_positions, expected_weight",
    (
        (("O.", ".."), 2),
        (("O.", ".#", ".O"), 4),
    ),
)
def test_weight_for_positions_returns_total_weight(given_positions, expected_weight):
    weight = day_14.calculate_weight(given_positions)
    assert weight == expected_weight


@pytest.mark.parametrize(
    "given_sequence, expected_offset, expected_cycle",
    (
        ((1, 2, 3, 1, 2, 3), 0, (1, 2, 3)),
        ((1, 1, 2, 1, 1, 2), 0, (1, 1, 2)),
        ((1, 2, 3, 1, 0, 1, 1, 0, 1), 3, (1, 0, 1)),
        ((1, 2, 3, 1, 2, 3, 1, 2, 3, 1), 0, (1, 2, 3)),
        ((1, 2, 3, 4, 4, 5, 5, 4, 4, 5, 5, 4), 3, (4, 4, 5, 5)),
        ((1, 2, 3, 4, 5, 6, 7), None, None),
    ),
)
def test_find_cycle_in_list(given_sequence, expected_offset, expected_cycle):
    offset, cycle = day_14.find_cycle(given_sequence)
    assert cycle == expected_cycle
    assert offset == expected_offset


def test_solving_part_one_gives_expected_value():
    answer = day_14.solve_part_one(TEST_INPUT_1)
    expected_answer = 136
    assert answer == expected_answer


def test_solving_part_two_gives_expected_value():
    answer = day_14.solve_part_two(TEST_INPUT_1)
    expected_answer = 64
    assert answer == expected_answer
