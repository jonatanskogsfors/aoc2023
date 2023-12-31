from pathlib import Path

import pytest
from aoc2023 import day_3
from aoc2023.day_3 import ItemPosition

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_3_1.txt"


def test_parse_input_returns_tuple_of_strings():
    parsed_schematic = day_3.parse_input(TEST_INPUT_1)

    assert parsed_schematic
    assert isinstance(parsed_schematic, tuple)

    expected_rows_in_schematic = 10
    assert len(parsed_schematic) == expected_rows_in_schematic

    expected_columns_in_schematic = 10
    assert all(len(row) == expected_columns_in_schematic for row in parsed_schematic)


@pytest.mark.parametrize(
    "given_number, expected_indices",
    (
        (ItemPosition(1, 0, 0), {(0, 1), (1, 0), (1, 1)}),  # Corner case
        (ItemPosition(12, 0, 0), {(2, 0), (0, 1), (1, 1), (2, 1)}),
        (
            ItemPosition(3, 1, 1),
            {(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)},
        ),
    ),
)
def test_adjacent_indices_returns_indices_around_number(given_number, expected_indices):
    assert day_3.adjacent_indices(given_number) == expected_indices


@pytest.mark.parametrize(
    "given_number, expected_symbol",
    (
        (ItemPosition(467, 0, 0), ItemPosition("*", 3, 1)),
        (ItemPosition(114, 5, 0), None),
        (ItemPosition(617, 0, 4), ItemPosition("*", 3, 4)),
        (ItemPosition(592, 2, 6), ItemPosition("+", 5, 5)),
        (ItemPosition(58, 7, 5), None),
    ),
)
def test_adjacent_symbol_finds_expected_symbol(
    given_number: ItemPosition, expected_symbol
):
    given_schematic = day_3.parse_input(TEST_INPUT_1)

    assert day_3.adjacent_symbol(given_number, given_schematic) == expected_symbol


def test_find_numbers_in_schematic():
    given_schematic = day_3.parse_input(TEST_INPUT_1)

    numbers = day_3.numbers_in_schematic(given_schematic)

    expected_numbers = {
        ItemPosition(467, 0, 0),
        ItemPosition(114, 5, 0),
        ItemPosition(35, 2, 2),
        ItemPosition(633, 6, 2),
        ItemPosition(617, 0, 4),
        ItemPosition(58, 7, 5),
        ItemPosition(592, 2, 6),
        ItemPosition(755, 6, 7),
        ItemPosition(664, 1, 9),
        ItemPosition(598, 5, 9),
    }

    assert numbers == expected_numbers


def test_cogs_in_schematic_finds_all_cogs():
    given_schematic = day_3.parse_input(TEST_INPUT_1)

    cogs = day_3.cogs_in_schematics(given_schematic)

    expected_cogs = {
        ItemPosition(16345, 3, 1),
        ItemPosition(451490, 5, 8),
    }

    assert cogs == expected_cogs


def test_solving_part_one_gives_expected_value():
    answer = day_3.solve_part_one(TEST_INPUT_1)
    expected_answer = 4361
    assert answer == expected_answer


def test_solving_part_two_gives_expected_value():
    answer = day_3.solve_part_two(TEST_INPUT_1)
    expected_answer = 467835
    assert answer == expected_answer
