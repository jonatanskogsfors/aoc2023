from pathlib import Path


def main():
    input_path = Path("input/input_10.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))


def parse_input(input_path: Path) -> tuple[str]:
    return tuple(input_path.read_text().splitlines())


def find_start(sketch: tuple[str, ...]):
    for y, row in enumerate(sketch):
        if (x := row.find("S")) != -1:
            return x, y
    return None


def connections(sketch: tuple[str], current_position: tuple[int, int]):
    pipes = {
        "|": {(0, -1), (0, 1)},
        "-": {(-1, 0), (1, 0)},
        "L": {(1, 0), (0, -1)},
        "J": {(-1, 0), (0, -1)},
        "7": {(-1, 0), (0, 1)},
        "F": {(0, 1), (1, 0)},
        "S": {(1, 0), (0, 1), (-1, 0), (0, -1)},
    }
    x, y = current_position
    current_pipe = sketch[y][x]
    if current_pipe == "S":
        return {
            position
            for position in {
                (x + x_delta, y + y_delta)
                for x_delta, y_delta in pipes.get(current_pipe, set())
            }
            if current_position in connections(sketch, position)
        }
    return {
        (x + x_delta, y + y_delta) for x_delta, y_delta in pipes.get(current_pipe, set())
    }


def enclosed_tiles(loop: tuple[tuple[int, int]]) -> set[tuple[int, int]]:
    max_x = max(position[0] for position in loop)
    min_x = min(position[0] for position in loop)
    max_y = max(position[1] for position in loop)
    min_y = min(position[1] for position in loop)

    enclosed = set()
    for position in [
        (x, y)
        for y in range(min_y, max_y + 1)
        for x in range(min_x, max_x + 1)
        if (x, y) not in loop
    ]:
        if is_inside(position, loop):
            enclosed.add(position)
    return enclosed


def is_inside(position, loop):
    rows_in_vertical_line = 3
    crossings = []
    y = position[1]
    local_loop = set()
    for x, y in [(x, y) for x in reversed(range(position[0]))]:
        test_position = (x, y)
        if test_position not in local_loop:
            if len({position[1] for position in local_loop}) == rows_in_vertical_line:
                # We have moved passed a vertical line
                crossings.append((x + 1, y))
            local_loop = set()

        if test_position in loop:
            loop_index = loop.index(test_position)
            local_loop.update(get_local_loop(loop, loop_index))

            if len({position[1] for position in local_loop}) == rows_in_vertical_line:
                crossings.append(test_position)
                local_loop = set()
    return len(crossings) % 2 == 1


def get_local_loop(loop, loop_index) -> set[tuple[int, int]]:
    previous_index = loop_index - 1
    next_index = loop_index + 1 if loop_index < len(loop) - 1 else 0
    local_loop = {
        position
        for position in (loop[loop_index], loop[previous_index], loop[next_index])
    }
    return local_loop


def get_loop(sketch: tuple[str]) -> tuple[tuple[int, int]]:
    start_position = find_start(sketch)
    position = next(iter(connections(sketch, start_position)))
    visited = [start_position, position]
    while positions := [
        connection
        for connection in connections(sketch, position)
        if connection not in visited
    ]:
        position = positions[0]
        visited.append(position)
    return tuple(visited)


def solve_part_one(input_path: Path):
    sketch = parse_input(input_path)
    loop = get_loop(sketch)
    return len(loop) // 2


def solve_part_two(input_path: Path):
    sketch = parse_input(input_path)
    loop = get_loop(sketch)
    tiles = enclosed_tiles(loop)
    return len(tiles)


if __name__ == "__main__":
    main()
