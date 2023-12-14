import enum
from collections import deque
from pathlib import Path


def main():
    input_path = Path("input/input_14.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))


class Direction(enum.Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 4


def calculate_weight(positions):
    return sum(row.count("O") * n for n, row in enumerate(reversed(positions), start=1))


def parse_input(input_path: Path):
    return tuple(input_path.read_text().split())


def tilt_platform(positions: tuple[str, ...], direction=Direction.NORTH):
    match direction:
        case Direction.NORTH:
            transposed_positions = list("".join(reversed(row)) for row in zip(*positions))
        case Direction.WEST:
            transposed_positions = list("".join(reversed(row)) for row in positions)
        case Direction.SOUTH:
            transposed_positions = list("".join(row) for row in zip(*positions))
        case Direction.EAST:
            transposed_positions = list(positions)

    for n, column in enumerate(transposed_positions):
        between_the_cubes = ["".join(sorted(space)) for space in column.split("#")]
        transposed_positions[n] = "#".join(between_the_cubes)

    match direction:
        case Direction.NORTH:
            positions = [
                "".join(row)
                for row in zip(*[reversed(column) for column in transposed_positions])
            ]
        case Direction.WEST:
            positions = ["".join(reversed(row)) for row in transposed_positions]
        case Direction.SOUTH:
            positions = ["".join(row) for row in zip(*transposed_positions)]
        case Direction.EAST:
            positions = transposed_positions

    return tuple(positions)


def spin_cycle(positions, spin_cycles):
    for _ in range(spin_cycles):
        for direction in (
            Direction.NORTH,
            Direction.WEST,
            Direction.SOUTH,
            Direction.EAST,
        ):
            positions = tilt_platform(positions, direction)
    return positions


def find_cycle(sequence, minimum_length=3):
    sequence_end = len(sequence)
    cycle = deque()
    for cycle_start in reversed(range(sequence_end - minimum_length + 1)):
        cycle_candidate = sequence[cycle_start:]
        cycle_length = sequence_end - cycle_start
        next_cycle = sequence[cycle_start - cycle_length : sequence_end - cycle_length]
        if cycle_candidate == next_cycle:
            cycle = deque(cycle_candidate)
            break
    else:
        return None, None
    for n, _ in enumerate(sequence):
        for _ in range(len(cycle)):
            offset_candidate = tuple(sequence[n : n + cycle_length])
            if offset_candidate == tuple(cycle):
                return n, tuple(cycle)
            cycle.rotate(1)


def solve_part_one(input_path: Path):
    positions = parse_input(input_path)
    positions = tilt_platform(positions)
    return calculate_weight(positions)


def solve_part_two(input_path: Path):
    positions = parse_input(input_path)
    weights = [calculate_weight(positions)]
    for n in range(500):
        positions = spin_cycle(positions, 1)
        weights.append(calculate_weight(positions))
        offset, cycle = find_cycle(weights)
        if cycle is not None:
            cycle_index = (1_000_000_000 - offset) % len(cycle)
            return cycle[cycle_index]
    return None


if __name__ == "__main__":
    main()
