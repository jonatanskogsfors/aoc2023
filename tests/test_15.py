from pathlib import Path

import pytest
from aoc2023 import day_15

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_15_1.txt"


@pytest.mark.parametrize(
    "given_string, expected_hash",
    (
        ("HASH", 52),
        ("rn=1", 30),
        ("cm-", 253),
        ("qp=3", 97),
        ("cm=2", 47),
        ("qp-", 14),
        ("pc=4", 180),
        ("ot=9", 9),
        ("ab=5", 197),
        ("pc-", 48),
        ("pc=6", 214),
        ("ot=7", 231),
    ),
)
def test_hash_for_strings(given_string, expected_hash):
    hash = day_15.hash_string(given_string)
    assert hash == expected_hash


def test_parse_input_returns_tuple_of_strings():
    parsed_input = day_15.parse_input(TEST_INPUT_1)

    assert parsed_input
    assert isinstance(parsed_input, tuple)
    assert all(isinstance(element, str) for element in parsed_input)
    assert all("\n" not in element for element in parsed_input)


@pytest.mark.parametrize(
    "given_hash_map, given_instruction, expected_hashmap",
    (
        ({}, "rn=1", {0: {"rn": 1}}),
        ({0: {"rn": 1}}, "cm-", {0: {"rn": 1}}),
        ({0: {"rn": 1}}, "qp=3", {0: {"rn": 1}, 1: {"qp": 3}}),
        ({0: {"rn": 1}, 1: {"qp": 3}}, "cm=2", {0: {"rn": 1, "cm": 2}, 1: {"qp": 3}}),
        ({0: {"rn": 1, "cm": 2}, 1: {"qp": 3}}, "qp-", {0: {"rn": 1, "cm": 2}}),
        ({}, "longerlabel=1", {55: {"longerlabel": 1}}),
        ({55: {"longerlabel": 1}}, "longerlabel-", {}),
    ),
)
def test_instruction_affects_hashmap(given_hash_map, given_instruction, expected_hashmap):
    new_hashmap = day_15.initialization_step(given_instruction, given_hash_map)
    assert new_hashmap == expected_hashmap


def test_solving_part_one_gives_expected_value():
    answer = day_15.solve_part_one(TEST_INPUT_1)
    expected_answer = 1320
    assert answer == expected_answer


def test_solving_part_two_gives_expected_value():
    answer = day_15.solve_part_two(TEST_INPUT_1)
    expected_answer = 145
    assert answer == expected_answer
