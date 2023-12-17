from pathlib import Path

from aoc2023 import day_16
from aoc2023.direction import Direction
from aoc2023.position import Position

TEST_INPUT_DIR = Path(__file__).parent / "test_input"
TEST_INPUT_1 = TEST_INPUT_DIR / "test_input_16_1.txt"


class TestDay16:
    def setup_method(self):
        day_16.loop_catcher = set()

    def test_unobtstucted_light_goes_straight(self):
        given_contraption = ("...", "...", "...")
        given_start_position = Position(0, 0)
        given_start_direction = Direction.RIGHT

        beam = day_16.trace_beam(
            given_start_position, given_start_direction, given_contraption
        )
        expected_beam = {
            (Position(0, 0), Direction.RIGHT),
            (Position(1, 0), Direction.RIGHT),
            (Position(2, 0), Direction.RIGHT),
        }
        assert beam == expected_beam

    def test_light_bounces_on_angled_mirrors(self):
        given_contraption = (r".\.", "...", "./.")
        given_start_position = Position(0, 0)
        given_start_direction = Direction.RIGHT

        beam = day_16.trace_beam(
            given_start_position, given_start_direction, given_contraption
        )
        expected_beam = {
            (Position(0, 0), Direction.RIGHT),
            (Position(1, 0), Direction.RIGHT),
            (Position(1, 1), Direction.DOWN),
            (Position(1, 2), Direction.DOWN),
            (Position(0, 2), Direction.LEFT),
        }
        assert beam == expected_beam

    def test_light_ignores_pointy_side_off_splitter(self):
        given_contraption = ("._\\", "|.|", "\\-/")
        given_start_position = Position(0, 0)
        given_start_direction = Direction.RIGHT

        beam = day_16.trace_beam(
            given_start_position, given_start_direction, given_contraption
        )
        expected_beam = {
            (Position(0, 0), Direction.RIGHT),
            (Position(1, 0), Direction.RIGHT),
            (Position(2, 0), Direction.RIGHT),
            (Position(2, 1), Direction.DOWN),
            (Position(2, 2), Direction.DOWN),
            (Position(1, 2), Direction.LEFT),
            (Position(0, 2), Direction.LEFT),
            (Position(0, 1), Direction.UP),
            (Position(0, 0), Direction.UP),
        }
        assert beam == expected_beam

    def test_light_is_split_by_vertical_splitter(self):
        given_contraption = ("...", ".|.", "...")
        given_start_position = Position(0, 1)
        given_start_direction = Direction.RIGHT

        beam = day_16.trace_beam(
            given_start_position, given_start_direction, given_contraption
        )

        expected_beam = {
            (Position(0, 1), Direction.RIGHT),
            (Position(1, 1), Direction.RIGHT),
            (Position(1, 0), Direction.UP),
            (Position(1, 2), Direction.DOWN),
        }
        assert beam == expected_beam

    def test_light_is_split_by_horizontal_splitter(self):
        given_contraption = ("...", ".-.", "...")
        given_start_position = Position(1, 0)
        given_start_direction = Direction.DOWN

        beam = day_16.trace_beam(
            given_start_position, given_start_direction, given_contraption
        )

        expected_beam = {
            (Position(1, 0), Direction.DOWN),
            (Position(1, 1), Direction.DOWN),
            (Position(0, 1), Direction.LEFT),
            (Position(2, 1), Direction.RIGHT),
        }
        assert beam == expected_beam

    def test_trace_beam_with_loop(self):
        given_contraption = ("-\\", "\\/")
        given_start_position = Position(0, 0)
        given_start_direction = Direction.RIGHT

        beam = day_16.trace_beam(
            given_start_position, given_start_direction, given_contraption
        )

        expected_beam = {
            (Position(0, 0), Direction.RIGHT),
            (Position(1, 0), Direction.RIGHT),
            (Position(1, 1), Direction.DOWN),
            (Position(0, 1), Direction.LEFT),
            (Position(0, 0), Direction.UP),
        }
        assert beam == expected_beam

    def test_parse_input_returns_tuple_of_strings(self):
        parsed_input = day_16.parse_input(TEST_INPUT_1)

        assert parsed_input
        assert isinstance(parsed_input, tuple)
        assert all(isinstance(element, str) for element in parsed_input)

    def test_solving_part_one_gives_expected_value(self):
        answer = day_16.solve_part_one(TEST_INPUT_1)
        expected_answer = 46
        assert answer == expected_answer

    def test_solving_part_two_gives_expected_value(self):
        answer = day_16.solve_part_two(TEST_INPUT_1)
        expected_answer = 51
        assert answer == expected_answer
