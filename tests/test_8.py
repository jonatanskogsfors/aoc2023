from pathlib import Path

import pytest
from aoc2023 import day_8
from aoc2023.day_8 import Instruction

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_8_1.txt"
TEST_INPUT_2 = TEST_INPUT_DIR / "test_input_8_2.txt"
TEST_INPUT_3 = TEST_INPUT_DIR / "test_input_8_3.txt"


def test_parsing_input_returns_instructions_and_network():
    # Given an input path
    given_input_path = TEST_INPUT_1

    # When parsing the input
    parsed_input = day_8.parse_input(given_input_path)

    # Then the parsed input has two elements, instructions and network
    expected_input_elements = 2
    assert len(parsed_input) == expected_input_elements
    instructions, network = parsed_input

    # And instructions and network are not empty
    assert instructions
    assert network

    # And instructions and network are the expected types
    assert isinstance(instructions, tuple)
    assert isinstance(network, dict)

    # And instructions and network elements are the expected types
    assert all(isinstance(instruction, Instruction) for instruction in instructions)
    assert all(isinstance(node, str) for node in network.keys())
    assert all(isinstance(nodes, tuple) for nodes in network.values())
    assert all(
        isinstance(node, str)
        for node in [node for nodes in network.values() for node in nodes]
    )


@pytest.mark.parametrize(
    "given_start_node, given_network, given_instructions, expected_before_cycle, "
    "expected_period",
    (
        (
            "AAA",
            {
                "AAA": ("BBB", "CCC"),
                "BBB": ("DDD", "ZZZ"),
                "CCC": ("AAA", "DDD"),
                "DDD": ("ZZZ", "BBB"),
                "ZZZ": ("CCC", "BBB"),
            },
            (Instruction.L, Instruction.L, Instruction.R),
            5,
            3,
        ),
    ),
)
def test_find_cycle_returns_expected_start_and_cycle_length(
    given_start_node,
    given_network,
    given_instructions,
    expected_before_cycle,
    expected_period,
):
    before_cycle, period = day_8.find_cycle(
        given_start_node, given_instructions, given_network
    )
    assert before_cycle == expected_before_cycle
    assert period == expected_period


@pytest.mark.parametrize(
    "given_input_path, expected_answer", ((TEST_INPUT_1, 2), (TEST_INPUT_2, 6))
)
def test_solving_part_one_gives_expected_value(given_input_path, expected_answer):
    answer = day_8.solve_part_one(given_input_path)
    assert answer == expected_answer


def test_solving_part_two_gives_expected_value():
    answer = day_8.solve_part_two(TEST_INPUT_3)
    expected_answer = 6
    assert answer == expected_answer
