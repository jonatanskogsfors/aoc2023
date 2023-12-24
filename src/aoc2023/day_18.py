import collections
import re
from itertools import pairwise
from pathlib import Path

from aoc2023.direction import Direction
from aoc2023.position import Position


def main():
    input_path = Path("input/input_18.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))


def parse_input(input_path: Path, bug_fix=False):
    dig_pattern = re.compile(r"([LRUD]) (\d+) \((#[0-9a-f]{6})\)")
    dig_plan = []
    for row in input_path.read_text().splitlines():
        if match := dig_pattern.match(row):
            match match.group(1):
                case "U":
                    direction = Direction.UP
                case "R":
                    direction = Direction.RIGHT
                case "D":
                    direction = Direction.DOWN
                case "L":
                    direction = Direction.LEFT
            length = int(match.group(2))
            color = match.group(3)
            if bug_fix:
                direction, length = instruction_from_color(color)
            dig_plan.append((direction, length, color))
    return dig_plan


def create_bounding_box(dig_plan):
    current_x = 0
    current_y = 0
    corners = find_corners(current_x, current_y, dig_plan)
    x_values = [position.x for position in corners]
    y_values = [position.y for position in corners]

    min_x = min(x_values)
    width = max(x_values) - min_x + 1
    min_y = min(y_values)
    height = max(y_values) - min_y + 1
    bounding_box = []
    for _ in range(height):
        bounding_box.append("." * width)
    return bounding_box, Position(min_x, min_y)


def find_corners(current_x, current_y, dig_plan):
    corners = [Position(current_x, current_y)]
    for direction, length, _ in dig_plan:
        current_y += direction.delta().y * length
        current_x += direction.delta().x * length
        corners.append(Position(current_x, current_y))
    return corners


def create_outline(dig_plan):
    lagoon, offset = create_bounding_box(dig_plan)
    position = Position(abs(offset.x), abs(offset.y))
    for direction, length, _ in dig_plan:
        lagoon, position = dig_trench(lagoon, position, direction, length)

    return lagoon


def dig_trench(lagoon, position, direction, length):
    editable_lagoon = tuple(list(row) for row in lagoon)
    editable_lagoon[position.y][position.x] = "#"
    for n in range(length):
        position += direction.delta()
        editable_lagoon[position.y][position.x] = "#"
    return tuple("".join(row) for row in editable_lagoon), position


def flood_fill(lagoon, start_position):
    if not is_inside(lagoon, start_position):
        return lagoon
    height = len(lagoon)
    width = len(lagoon[0])
    editable_lagoon = tuple(list(row) for row in lagoon)
    fill_queue = collections.deque()
    fill_queue.append(start_position)
    while fill_queue:
        position = fill_queue.popleft()
        if editable_lagoon[position.y][position.x] == "#":
            continue
        editable_lagoon[position.y][position.x] = "#"
        if (left := position + Direction.LEFT.delta()).x >= 0:
            fill_queue.append(left)
        if (right := position + Direction.RIGHT.delta()).x < width:
            fill_queue.append(right)
        if (up := position + Direction.UP.delta()).y >= 0:
            fill_queue.append(up)
        if (down := position + Direction.DOWN.delta()).y < height:
            fill_queue.append(down)
    return tuple("".join(row) for row in editable_lagoon)


def faux_fill(dig_plan):
    corners = find_corners(0, 0, dig_plan)

    # Pixel shoelace formula
    criss = 0
    cross = 0
    for left, right in pairwise(reversed(corners)):
        criss += right.x * left.y
        cross += (left.x - 0) * (right.y - 0)

    inner_area = abs(criss - cross) // 2
    boundary = sum(length for _, length, _ in dig_plan)
    return inner_area + boundary // 2 + 1


def is_inside(lagoon, position) -> bool:
    return (
        len(
            [
                boundary
                for boundary in lagoon[position.y][: position.y].split(".")
                if boundary == "#"
            ]
        )
        % 2
        == 1
    )


def instruction_from_color(color):
    length = int(color[1:-1], 16)
    direction_index = int(color[-1], 16)
    direction = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP][
        direction_index
    ]
    return direction, length


def solve_part_one(input_path: Path):
    dig_plan = parse_input(input_path)
    outline = create_outline(dig_plan)
    height = len(outline)
    width = len(outline[0])
    start_position = Position(width // 2, height // 2)
    while not is_inside(outline, start_position):
        start_position += Direction.LEFT.delta()
    if start_position.x < 0:
        raise Exception("Oops")
    lagoon = flood_fill(outline, start_position)
    return sum(row.count("#") for row in lagoon)


def solve_part_two(input_path: Path):
    dig_plan = parse_input(input_path, bug_fix=True)
    return faux_fill(dig_plan)


if __name__ == "__main__":
    main()
