from pathlib import Path

import pytest
from aoc2023 import day_20
from aoc2023.day_20 import FlipFlopState, Pulse, PulseMessage

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_20_1.txt"
TEST_INPUT_2 = TEST_INPUT_DIR / "test_input_20_2.txt"


@pytest.mark.parametrize(
    "given_state, given_pulse, expected_pulses, expected_state",
    (
        (FlipFlopState.OFF, Pulse.HIGH, [], FlipFlopState.OFF),
        (FlipFlopState.OFF, Pulse.LOW, [Pulse.HIGH], FlipFlopState.ON),
        (FlipFlopState.ON, Pulse.HIGH, [], FlipFlopState.ON),
        (FlipFlopState.ON, Pulse.LOW, [Pulse.LOW], FlipFlopState.OFF),
    ),
)
def test_flip_flop_module(given_state, given_pulse, expected_pulses, expected_state):
    # Given a flip flop module with a given state
    given_flip_flop_module = day_20.FlipFlop("Flipper", given_state)

    # Given a mocked downstream module
    given_flip_flop_module.connect_output("Listener")

    # When a pulse is received
    pulse_messages = given_flip_flop_module.receive(given_pulse, "?")

    # Then the expected pulse (if any) is emitted
    assert [message.pulse for message in pulse_messages] == expected_pulses

    # And the state is as expected
    assert given_flip_flop_module.state == expected_state


def test_conjunction_module():
    # Given conjunction module
    given_conjunction_module = day_20.Conjunction("Conjunction")

    # Given two upstream modules
    given_conjunction_module.connect_input("Emitter1")
    given_conjunction_module.connect_input("Emitter2")

    # Given one downstream module
    given_conjunction_module.connect_output("Listener")

    # When the first module emits a high pulse
    pulse_messages = given_conjunction_module.receive(Pulse.HIGH, "Emitter1")

    # Then the conjunction module emits a high pulse
    assert pulse_messages[0] == PulseMessage("Conjunction", Pulse.HIGH, "Listener")

    # When the second module emits a high pulse
    pulse_messages = given_conjunction_module.receive(Pulse.HIGH, "Emitter2")

    # Then the conjunction module emits a low pulse
    assert pulse_messages[0] == PulseMessage("Conjunction", Pulse.LOW, "Listener")


def test_broadcaster_module():
    # Given broadcast module
    given_conjunction_module = day_20.Broadcast("Broadcaster")

    # Given one upstream modules
    given_conjunction_module.connect_input("Emitter")

    # Given three downstream module
    given_conjunction_module.connect_output("Listener1")
    given_conjunction_module.connect_output("Listener2")
    given_conjunction_module.connect_output("Listener3")

    # When the conjunction module receives a high pulse
    pulse_messages = given_conjunction_module.receive(Pulse.HIGH, "Emitter")

    # Then the conjunction module emits a high pulse to all outputs
    assert pulse_messages[0] == PulseMessage("Broadcaster", Pulse.HIGH, "Listener1")
    assert pulse_messages[1] == PulseMessage("Broadcaster", Pulse.HIGH, "Listener2")
    assert pulse_messages[2] == PulseMessage("Broadcaster", Pulse.HIGH, "Listener3")

    # When the conjunction module receives a low pulse
    pulse_messages = given_conjunction_module.receive(Pulse.LOW, "Emitter")

    # Then the conjunction module emits a low pulse to all outputs
    assert pulse_messages[0] == PulseMessage("Broadcaster", Pulse.LOW, "Listener1")
    assert pulse_messages[1] == PulseMessage("Broadcaster", Pulse.LOW, "Listener2")
    assert pulse_messages[2] == PulseMessage("Broadcaster", Pulse.LOW, "Listener3")


def test_button_module():
    # Given a button module
    given_button_module = day_20.Button("Button")

    # Given a downstream module
    given_button_module.connect_output("Listener")

    # When pushing the button
    pulse_messages = given_button_module.push()

    # Then a low pulse is sent to the listener
    assert pulse_messages == [PulseMessage("Button", Pulse.LOW, "Listener")]


def test_parse_input():
    # When parsing input
    parsed_input = day_20.parse_input(TEST_INPUT_1)

    # Then result is a dictionary
    assert isinstance(parsed_input, dict)

    # And the dictionary has a broadcaster
    assert "broadcaster" in parsed_input
    assert type(parsed_input["broadcaster"]) is day_20.Broadcast

    # And the dictionary has a button
    assert "button" in parsed_input
    assert type(parsed_input["button"]) is day_20.Button

    # And the button is connected to the broadcaster
    assert parsed_input["button"].outputs == ["broadcaster"]


@pytest.mark.parametrize(
    "given_input_path, expected_low_pulses, expected_high_pulses",
    ((TEST_INPUT_1, 8, 4), (TEST_INPUT_2, 4, 4)),
)
def test_press_button_once_gives_the_expected_outcome(
    given_input_path, expected_low_pulses, expected_high_pulses
):
    # Given modules
    given_modules = day_20.parse_input(given_input_path)

    # Given a dispatcher
    given_dispatcher = day_20.Dispatcher(given_modules)

    # When pressing button
    low_pulses, high_pulses = given_dispatcher.push_button()

    # Then the expected number of pulses are sent
    assert low_pulses == expected_low_pulses
    assert high_pulses == expected_high_pulses


@pytest.mark.parametrize(
    "given_input_path, expected_answer",
    ((TEST_INPUT_1, 32000000), (TEST_INPUT_2, 11687500)),
)
def test_solving_part_one_gives_expected_value(given_input_path, expected_answer):
    answer = day_20.solve_part_one(given_input_path)
    assert answer == expected_answer
