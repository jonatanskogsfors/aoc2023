from pathlib import Path

from aoc2023.direction import Direction
from aoc2023.position import Position

loop_catcher = set()


def main():
    input_path = Path("input/input_16.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))  # 8243 (low)


def index_contraption(contraption: tuple[str, ...], position: Position):
    return contraption[position.y][position.x]


def trace_beam(position: Position, direction: Direction, contraption: tuple[str, ...]):
    if (position, direction) in loop_catcher:
        return set()
    else:
        loop_catcher.add((position, direction))

    contraption_height = len(contraption)
    contraption_width = len(contraption[0])
    beam = set()

    while 0 <= position.x < contraption_width and 0 <= position.y < contraption_height:
        beam.add((position, direction))
        match index_contraption(contraption, position), direction:
            case (
                ("/", (Direction.LEFT | Direction.RIGHT))
                | ("\\", (Direction.DOWN | Direction.UP))
            ):
                direction = Direction((direction.value - 1) % 4)
            case (
                ("\\", (Direction.LEFT | Direction.RIGHT))
                | ("/", (Direction.DOWN | Direction.UP))
            ):
                direction = Direction((direction.value + 1) % 4)
            case "|", (Direction.LEFT | Direction.RIGHT):
                return (
                    beam
                    | trace_beam(
                        position + Direction.UP.delta(), Direction.UP, contraption
                    )
                    | trace_beam(
                        position + Direction.DOWN.delta(), Direction.DOWN, contraption
                    )
                )
            case "-", (Direction.UP | Direction.DOWN):
                return (
                    beam
                    | trace_beam(
                        position + Direction.LEFT.delta(), Direction.LEFT, contraption
                    )
                    | trace_beam(
                        position + Direction.RIGHT.delta(), Direction.RIGHT, contraption
                    )
                )

        new_position = position + direction.delta()
        position = new_position

    return beam


def parse_input(input_path: Path):
    return tuple(input_path.read_text().split())


def solve_part_one(input_path: Path):
    contraption = parse_input(input_path)
    start_position = Position(0, 0)
    start_direction = Direction.RIGHT
    beam = trace_beam(start_position, start_direction, contraption)
    return len({position for position, direction in beam})


def solve_part_two(input_path: Path):
    contraption = parse_input(input_path)
    width = len(contraption[0])
    height = len(contraption)
    left_edge = {(Position(0, y), Direction.RIGHT) for y in range(height)}
    right_edge = {(Position(width - 1, y), Direction.LEFT) for y in range(height)}
    top_edge = {(Position(x, 0), Direction.DOWN) for x in range(width)}
    bottom_edge = {(Position(x, height - 1), Direction.UP) for x in range(height)}
    start_configurations = left_edge | right_edge | top_edge | bottom_edge
    max_energy = 0
    for start_position, start_direction in start_configurations:
        global loop_catcher
        loop_catcher = set()
        beam = trace_beam(start_position, start_direction, contraption)
        max_energy = max(max_energy, len({position for position, direction in beam}))
    return max_energy


if __name__ == "__main__":
    main()
