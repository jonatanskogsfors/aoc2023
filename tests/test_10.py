from pathlib import Path

import pytest
from aoc2023 import day_10

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_10_1.txt"
TEST_INPUT_2 = TEST_INPUT_DIR / "test_input_10_2.txt"
TEST_INPUT_3 = TEST_INPUT_DIR / "test_input_10_3.txt"
TEST_INPUT_4 = TEST_INPUT_DIR / "test_input_10_4.txt"
TEST_INPUT_5 = TEST_INPUT_DIR / "test_input_10_5.txt"


def test_parse_input_returns_tuple_of_strings():
    sketch = day_10.parse_input(TEST_INPUT_1)

    expected_rows = 5
    assert len(sketch) == expected_rows
    assert isinstance(sketch, tuple)
    expected_columns = 5
    assert all(len(row) == expected_columns for row in sketch)
    assert all(isinstance(row, str) for row in sketch)


@pytest.mark.parametrize(
    "given_input_path, expected_start_coordinates",
    ((TEST_INPUT_1, (1, 1)), (TEST_INPUT_2, (0, 2))),
)
def test_locate_start_gives_expected_value(given_input_path, expected_start_coordinates):
    sketch = day_10.parse_input(given_input_path)
    start_position = day_10.find_start(sketch)
    assert start_position == expected_start_coordinates


@pytest.mark.parametrize(
    "given_input_path, given_position, expected_connections",
    (
        (TEST_INPUT_1, (2, 1), {(1, 1), (3, 1)}),
        (TEST_INPUT_1, (3, 1), {(2, 1), (3, 2)}),
        (TEST_INPUT_1, (1, 1), {(2, 1), (1, 2)}),
        (TEST_INPUT_1, (2, 2), set()),
    ),
)
def test_get_connections_for_pipe_gives_expected_directions(
    given_input_path, given_position, expected_connections
):
    sketch = day_10.parse_input(given_input_path)
    connections = day_10.connections(sketch, given_position)
    assert connections == expected_connections


@pytest.mark.parametrize(
    "given_input_path, expected_loop",
    ((TEST_INPUT_1, ((1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (1, 2))),),
)
def test_get_loop_returns_sequence_with_all_pipe_positions(
    given_input_path, expected_loop
):
    sketch = day_10.parse_input(given_input_path)
    loop = day_10.get_loop(sketch)
    reversed_expected_loop = expected_loop[0:1] + tuple(reversed(expected_loop[1:]))
    assert loop in (expected_loop, reversed_expected_loop)


@pytest.mark.parametrize(
    "given_input_path, given_position, expected_status",
    (
        (TEST_INPUT_1, (2, 2), True),
        (TEST_INPUT_1, (0, 2), False),
        (TEST_INPUT_2, (2, 2), True),
        (TEST_INPUT_3, (2, 6), True),
        (TEST_INPUT_3, (5, 5), False),
        (TEST_INPUT_3, (5, 6), False),
        (TEST_INPUT_4, (6, 6), True),
        (TEST_INPUT_4, (3, 2), False),
        (TEST_INPUT_4, (14, 3), True),
        (TEST_INPUT_4, (9, 8), False),
        (TEST_INPUT_4, (19, 4), False),
    ),
)
def test_is_inside_returns_correct_status(
    given_input_path: Path, given_position: tuple[int, int], expected_status
):
    sketch = day_10.parse_input(given_input_path)
    loop = day_10.get_loop(sketch)
    inside = day_10.is_inside(given_position, loop)
    assert inside == expected_status


@pytest.mark.parametrize(
    "given_input_path, expected_answer", ((TEST_INPUT_1, 4), (TEST_INPUT_2, 8))
)
def test_solving_part_one_gives_expected_value(given_input_path, expected_answer):
    answer = day_10.solve_part_one(given_input_path)
    assert answer == expected_answer


@pytest.mark.parametrize(
    "given_input_path, expected_answer",
    ((TEST_INPUT_3, 4), (TEST_INPUT_4, 8), (TEST_INPUT_5, 10)),
)
def test_solving_part_two_gives_expected_value(given_input_path, expected_answer):
    answer = day_10.solve_part_two(given_input_path)
    assert answer == expected_answer
