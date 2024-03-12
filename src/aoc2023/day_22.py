import dataclasses
from pathlib import Path

from aoc2023.position import Position, Position3d


@dataclasses.dataclass
class Square:
    corner_1: Position
    corner_2: Position


@dataclasses.dataclass
class Cube:
    corner_1: Position3d
    corner_2: Position3d

    @property
    def height(self):
        return self.corner_2.z - self.corner_1.z + 1


def main():
    input_path = Path("input/input_22.txt")
    print(solve_part_one(input_path))  # 565 -> _451_
    print(solve_part_two(input_path))


def parse_input(input_path: Path):
    cubes = []
    for row in input_path.read_text().strip().split("\n"):
        corner_1_input, corner_2_input = row.split("~")
        corner_1 = Position3d(*map(int, corner_1_input.split(",")))
        corner_2 = Position3d(*map(int, corner_2_input.split(",")))
        cubes.append(Cube(corner_1, corner_2))
    return tuple(cubes)


def project_cube(cube: Cube) -> Square:
    corner_1 = Position(cube.corner_1.x, cube.corner_1.y)
    corner_2 = Position(cube.corner_2.x, cube.corner_2.y)
    return Square(corner_1, corner_2)


def print_square(square: Square):
    rows = []
    for y in range(3):
        row = ""
        for x in range(3):
            if (square.corner_1.x <= x <= square.corner_2.x) and (
                square.corner_1.y <= y <= square.corner_2.y
            ):
                row += "X"
            else:
                row += "."
        rows.append(row)
    print("\n".join(rows))
    return rows


def is_overlapping(square_1: Square, square_2: Square):
    x1_min, x1_max = square_1.corner_1.x, square_1.corner_2.x
    x2_min, x2_max = square_2.corner_1.x, square_2.corner_2.x
    y1_min, y1_max = square_1.corner_1.y, square_1.corner_2.y
    y2_min, y2_max = square_2.corner_1.y, square_2.corner_2.y

    horizontal_overlap = (x1_min <= x2_min <= x1_max) or (x2_min <= x1_min <= x2_max)
    vertical_overlap = (y1_min <= y2_min <= y1_max) or (y2_min <= y1_min <= y2_max)

    return horizontal_overlap and vertical_overlap


def drop_cube(cube: Cube, new_level: int):
    cube.corner_2.z = new_level + (cube.height - 1)
    cube.corner_1.z = new_level
    return cube


def drop_all_cubes(snapshot: tuple[Cube, ...]):
    for cube in sorted(snapshot, key=lambda c: c.corner_1.z):
        cubes_below = sorted(
            (
                other_cube
                for other_cube in snapshot
                if other_cube.corner_2.z < cube.corner_1.z
            ),
            key=lambda c: c.corner_2.z,
            reverse=True,
        )
        if not cubes_below:
            drop_cube(cube, 1)
        dropped = False
        for lower_cube in cubes_below:
            if is_overlapping(project_cube(cube), project_cube(lower_cube)):
                drop_cube(cube, lower_cube.corner_2.z + 1)
                dropped = True
                break
        if not dropped:
            drop_cube(cube, 1)
    return snapshot


def is_disintegratable(cube: Cube, stack: tuple[Cube, ...]):
    same_layer = [
        other_cube
        for other_cube in stack
        if other_cube.corner_2.z == cube.corner_2.z and other_cube != cube
    ]

    supported_cubes = [
        other_cube
        for other_cube in stack
        if other_cube.corner_1.z - cube.corner_2.z == 1
        and is_overlapping(project_cube(cube), project_cube(other_cube))
    ]
    if not supported_cubes:
        return True

    if not same_layer:
        return False

    for supported_cube in supported_cubes:
        cosupporting_cubes = [
            other_cube
            for other_cube in same_layer
            if is_overlapping(project_cube(other_cube), project_cube(supported_cube))
        ]
        if not cosupporting_cubes:
            return False
    return True


def solve_part_one(input_path: Path):
    snapshot = parse_input(input_path)
    stack = drop_all_cubes(snapshot)
    disintegratable = [cube for cube in stack if is_disintegratable(cube, stack)]
    return len(disintegratable)


def solve_part_two(input_path: Path):
    ...


if __name__ == "__main__":
    main()
