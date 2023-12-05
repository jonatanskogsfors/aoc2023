from pathlib import Path

import pytest

from aoc2023 import day_5
from aoc2023.day_5 import CategoryRange, CategoryMap

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_5_1.txt"


@pytest.mark.parametrize(
    "given_ranges, given_source, expected_destination",
    (
        ((CategoryRange(50, 98, 2), CategoryRange(52, 50, 48)), 79, 81),
        ((CategoryRange(50, 98, 2), CategoryRange(52, 50, 48)), 14, 14),
        ((CategoryRange(50, 98, 2), CategoryRange(52, 50, 48)), 55, 57),
        ((CategoryRange(50, 98, 2), CategoryRange(52, 50, 48)), 13, 13),
    )
)
def test_convert_to_category_gives_correct_value(given_ranges, given_source, expected_destination):
    _, category_map = CategoryMap(*given_ranges)
    destination = category_map.convert(given_source)
    assert destination == expected_destination


@pytest.mark.parametrize(
    "given_source, expected_destination",
    ((79, 82), (14, 43), (55, 86), (13, 35))
)
def test_connected_maps_gives_correct_value(given_source, expected_destination):
    connected_map = day_5.parse_input(TEST_INPUT_1)
    destination = connected_map.convert(given_source)
    assert destination == expected_destination