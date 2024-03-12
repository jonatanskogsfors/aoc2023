from pathlib import Path

import pytest
from aoc2023 import day_22
from aoc2023.day_22 import Cube, Square
from aoc2023.position import Position, Position3d

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_22_1.txt"
TEST_INPUT_2 = TEST_INPUT_DIR / "test_input_22_2.txt"


@pytest.mark.parametrize(
    "given_cube, expected_square",
    (
        (
            Cube(Position3d(2, 2, 2), Position3d(2, 2, 2)),
            Square(Position(2, 2), Position(2, 2)),
        ),
        (
            Cube(Position3d(0, 0, 10), Position3d(1, 0, 10)),
            Square(Position(0, 0), Position(1, 0)),
        ),
        (
            Cube(Position3d(0, 0, 10), Position3d(0, 1, 10)),
            Square(Position(0, 0), Position(0, 1)),
        ),
        (
            Cube(Position3d(0, 0, 1), Position3d(0, 0, 10)),
            Square(Position(0, 0), Position(0, 0)),
        ),
    ),
)
def test_project_cube_gives_expected_value(given_cube, expected_square):
    projected_square = day_22.project_cube(given_cube)
    assert projected_square == expected_square


@pytest.mark.parametrize(
    "given_square_1, given_square_2, expected_overlap",
    (
        (
            Square(Position(0, 0), Position(0, 0)),
            Square(Position(0, 0), Position(0, 0)),
            True,
        ),
        (
            Square(Position(0, 0), Position(0, 0)),
            Square(Position(1, 1), Position(1, 1)),
            False,
        ),
        (
            Square(Position(0, 0), Position(2, 2)),
            Square(Position(2, 2), Position(4, 4)),
            True,
        ),
        (
            Square(Position(0, 0), Position(2, 2)),
            Square(Position(0, 3), Position(2, 5)),
            False,
        ),
    ),
)
def test_is_overlapping_finds_overlaps(given_square_1, given_square_2, expected_overlap):
    overlap = day_22.is_overlapping(given_square_1, given_square_2)
    assert overlap == expected_overlap


@pytest.mark.parametrize(
    "given_cube, expected_height",
    (
        (Cube(Position3d(1, 1, 1), Position3d(1, 1, 1)), 1),
        (Cube(Position3d(2, 3, 4), Position3d(5, 6, 7)), 4),
    ),
)
def test_cube_has_height(given_cube, expected_height):
    assert given_cube.height == expected_height


@pytest.mark.parametrize(
    "given_cube, given_new_level, expecter_cube",
    (
        (
            Cube(Position3d(1, 1, 1), Position3d(5, 5, 5)),
            1,
            Cube(Position3d(1, 1, 1), Position3d(5, 5, 5)),
        ),
        (
            Cube(Position3d(1, 2, 3), Position3d(1, 2, 3)),
            2,
            Cube(Position3d(1, 2, 2), Position3d(1, 2, 2)),
        ),
    ),
)
def test_drop_cube_updates_position(given_cube, given_new_level, expecter_cube):
    dropped_cube = day_22.drop_cube(given_cube, given_new_level)
    assert dropped_cube == expecter_cube


@pytest.mark.parametrize("given_input_path", (TEST_INPUT_1,))
def test_parse_input(given_input_path):
    parsed_input = day_22.parse_input(given_input_path)
    assert isinstance(parsed_input, tuple)
    assert all(isinstance(cube, Cube) for cube in parsed_input)


@pytest.mark.parametrize(
    "given_snapshot_path, expected_stack",
    (
        (
            TEST_INPUT_1,
            (
                Cube(Position3d(1, 0, 1), Position3d(1, 2, 1)),
                Cube(Position3d(0, 0, 2), Position3d(2, 0, 2)),
                Cube(Position3d(0, 2, 2), Position3d(2, 2, 2)),
                Cube(Position3d(0, 0, 3), Position3d(0, 2, 3)),
                Cube(Position3d(2, 0, 3), Position3d(2, 2, 3)),
                Cube(Position3d(0, 1, 4), Position3d(2, 1, 4)),
                Cube(Position3d(1, 1, 5), Position3d(1, 1, 6)),
            ),
        ),
    ),
)
def test_drop_all_cubes(given_snapshot_path, expected_stack):
    snapshot = day_22.parse_input(given_snapshot_path)
    stack = day_22.drop_all_cubes(snapshot)
    assert stack == expected_stack


@pytest.mark.parametrize(
    "given_cube, given_stack, expected_disintegratability",
    (
        (
            Cube(Position3d(0, 0, 0), Position3d(2, 0, 0)),
            (
                Cube(Position3d(0, 0, 0), Position3d(2, 0, 0)),
                Cube(Position3d(1, 0, 1), Position3d(1, 2, 1)),
            ),
            False,
        ),
        (
            Cube(Position3d(0, 0, 0), Position3d(2, 0, 0)),
            (
                Cube(Position3d(0, 0, 0), Position3d(2, 0, 0)),
                Cube(Position3d(0, 2, 0), Position3d(2, 2, 0)),
                Cube(Position3d(1, 0, 1), Position3d(1, 2, 1)),
            ),
            True,
        ),
    ),
)
def test_is_disintegratable_gives_expected_answer(
    given_cube, given_stack, expected_disintegratability
):
    disintegratable = day_22.is_disintegratable(given_cube, given_stack)
    assert disintegratable == expected_disintegratability


@pytest.mark.parametrize(
    "given_input_path, expected_answer", ((TEST_INPUT_1, 5), (TEST_INPUT_2, 3))
)
def test_solving_part_one_gives_expected_value(given_input_path, expected_answer):
    answer = day_22.solve_part_one(given_input_path)
    assert answer == expected_answer
