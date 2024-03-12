from pathlib import Path

from aoc2023.position import Position


def main():
    input_path = Path("input/input_21.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))


def parse_input(input_path: Path):
    return tuple(input_path.read_text().strip().split("\n"))


def solve_part_one(input_path: Path, steps: int = 64):
    garden_map = parse_input(input_path)
    positions = {get_start_position(garden_map)}
    for _ in range(steps):
        new_positions = set()
        for position in positions:
            new_positions |= get_possible_positions(position, garden_map)
        positions = new_positions
    return len(positions)


def solve_part_two(input_path: Path):
    ...


def get_position(position: Position, garden_map):
    return garden_map[position.y][position.x]


def get_start_position(garden_map):
    for n, row in enumerate(garden_map):
        for m, column in enumerate(row):
            if column == "S":
                return Position(m, n)


def position_possible(position, garden_map):
    max_y = len(garden_map)
    max_x = len(garden_map[0])
    return (
        0 <= position.x < max_x
        and 0 <= position.y < max_y
        and get_position(position, garden_map) != "#"
    )


def get_possible_positions(position: Position, garden_map: tuple[str, ...]):
    positions = {
        position + Position(0, -1),
        position + Position(-1, 0),
        position + Position(1, 0),
        position + Position(0, 1),
    }
    return {position for position in positions if position_possible(position, garden_map)}


if __name__ == "__main__":
    main()
