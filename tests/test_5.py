from pathlib import Path

import pytest

from aoc2023 import day_5
from aoc2023.day_5 import CategoryRange, CategoryMap, SeedRange

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_5_1.txt"


@pytest.mark.parametrize(
    "given_ranges, given_source, expected_destination",
    (
        ((CategoryRange(50, 98, 2), CategoryRange(52, 50, 48)), 79, 81),
        ((CategoryRange(50, 98, 2), CategoryRange(52, 50, 48)), 14, 14),
        ((CategoryRange(50, 98, 2), CategoryRange(52, 50, 48)), 55, 57),
        ((CategoryRange(50, 98, 2), CategoryRange(52, 50, 48)), 13, 13),
    ),
)
def test_convert_to_category_gives_correct_value(
    given_ranges, given_source, expected_destination
):
    category_map = CategoryMap(*given_ranges)
    destination = category_map.convert(given_source)
    assert destination == expected_destination


@pytest.mark.parametrize(
    "given_source, given_length, expected_source_end",
    (
        (0, 1, 0),
        (1, 2, 2),
        (2, 3, 4),
    ),
)
def test_category_range_calculates_source_end(
    given_source: int, given_length: int, expected_source_end: int
):
    given_range = CategoryRange(1337, given_source, given_length)
    assert given_range.source_end == expected_source_end


@pytest.mark.parametrize(
    "given_destination, given_length, expected_destination_end",
    (
        (0, 1, 0),
        (1, 2, 2),
        (2, 3, 4),
    ),
)
def test_category_range_calculates_destination_end(
    given_destination: int, given_length: int, expected_destination_end: int
):
    given_range = CategoryRange(given_destination, 1337, given_length)
    assert given_range.destination_end == expected_destination_end

    @pytest.mark.parametrize(
        "given_start, given_length, expected_end",
        (
            (0, 1, 0),
            (1, 2, 2),
            (2, 3, 4),
        ),
    )
    def test_seed_range_calculates_end(
        given_start: int, given_length: int, expected_end: int
    ):
        given_range = SeedRange(given_start, given_length)
        assert given_range.end == expected_end


@pytest.mark.parametrize(
    "given_source, expected_destination", ((79, 82), (14, 43), (55, 86), (13, 35))
)
def test_combined_maps_gives_correct_value(given_source, expected_destination):
    _, connected_map = day_5.parse_input(TEST_INPUT_1)
    destination = connected_map.convert(given_source)
    assert destination == expected_destination


@pytest.mark.parametrize(
    "given_left_range, given_right_range, expected_ranges",
    (
        (
            CategoryRange(1, 1, 4),
            CategoryRange(3, 3, 4),
            {CategoryRange(1, 1, 2), CategoryRange(3, 3, 2), CategoryRange(5, 5, 2)},
        ),
        (
            CategoryRange(51, 1, 10),
            CategoryRange(100, 60, 9),
            {CategoryRange(51, 1, 9), CategoryRange(100, 10, 1), CategoryRange(101, 61, 8)},
        ),
        (
            CategoryRange(10, 100, 20),
            CategoryRange(78, 8, 5),
            {CategoryRange(13, 103, 17), CategoryRange(80, 100, 3), CategoryRange(78, 8, 2)},
        ),
        (
            CategoryRange(20, 10, 20),
            CategoryRange(70, 100, 5),
            set(),
        ),
        (
            CategoryRange(50, 20, 5),
            CategoryRange(20, 50, 5),
            {CategoryRange(20, 20, 5)},
        ),
        (
            CategoryRange(50, 20, 10),
            CategoryRange(20, 50, 5),
            {CategoryRange(20, 20, 5), CategoryRange(55, 25, 5)},
        ),
        (
            CategoryRange(50, 20, 5),
            CategoryRange(14, 44, 11),
            {CategoryRange(20, 20, 5), CategoryRange(14, 44, 6)},
        ),
    ),
)
def test_split_overlapping_ranges(given_left_range, given_right_range, expected_ranges):
    checked, unchecked = day_5.split_ranges(given_left_range, given_right_range)
    disjunct_ranges = checked + unchecked
    assert set(disjunct_ranges) == expected_ranges


def test_combined_maps_can_convert_values():
    given_map_a = CategoryMap(CategoryRange(47, 32, 10), CategoryRange(1, 40, 5))

    given_map_b = CategoryMap(CategoryRange(98, 2, 7))

    given_map_a.combine(given_map_b)

    given_source = 42
    expected_destination = 99

    destination = given_map_a.convert(given_source)
    assert destination == expected_destination


@pytest.mark.parametrize(
    "given_seeds, expected_ranges",
    (((79, 14, 55, 13), {SeedRange(79, 14), SeedRange(55, 13)}),),
)
def test_seeds_to_range_returns_expected_range(given_seeds, expected_ranges):
    seed_ranges = day_5.seeds_to_ranges(given_seeds)
    assert set(seed_ranges) == expected_ranges


def test_solving_part_one_gives_expected_value():
    answer = day_5.solve_part_one(TEST_INPUT_1)
    expected_answer = 35
    assert answer == expected_answer


def test_solving_part_two_gives_expected_value():
    answer = day_5.solve_part_two(TEST_INPUT_1)
    expected_answer = 46
    assert answer == expected_answer
