import queue
from pathlib import Path

from aoc2023.direction import Direction
from aoc2023.position import Position


def main():
    input_path = Path("input/input_17.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))


def neighbors_for_node(graph, node: Position, direction: Direction, move_range=(1, 3)):
    width = len(graph[0])
    height = len(graph)

    if direction is None:
        new_directions = (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT)
    else:
        new_directions = (
            Direction((direction.value + 1) % 4),
            Direction((direction.value - 1) % 4),
        )

    neighbors = set()
    move_range_low, move_range_high = move_range
    for new_direction in new_directions:
        nodes_in_direction = [
            node_in_direction
            for n in range(move_range_low, move_range_high + 1)
            if 0 <= (node_in_direction := node + new_direction.delta() * n).x < width
            and 0 <= node_in_direction.y < height
        ]
        for node_in_direction in nodes_in_direction:
            cost = sum(
                index_graph(graph, node + new_direction.delta(), node_in_direction)
            )
            neighbors.add((cost, node_in_direction, new_direction))

    return sorted(neighbors)


def index_graph(graph, position_start: Position, position_end: Position = None):
    height = len(graph)
    width = len(graph[0])

    if position_end is not None:
        if position_start.x == position_end.x:
            up, down = sorted((position_start.y, position_end.y))
            return [graph[y][position_start.x] for y in range(up, down + 1)]
        if position_start.y == position_end.y:
            left, right = sorted((position_start.x, position_end.x))
            return [graph[position_start.y][x] for x in range(left, right + 1)]
        else:
            raise ValueError("Position ranges must be straight.")

    return graph[position_start.y][position_start.x]


def dijkstras_algorithm(graph, start: Position, goal: Position, move_range=(1, 3)):
    unvisited = queue.PriorityQueue()
    unvisited.put((0, start, None))
    visited = set()
    shortest = {(start, None): 0}
    while unvisited:
        node_cost, node_position, node_direction = unvisited.get()
        node_state = (node_position, node_direction)
        if node_position == goal:
            return shortest[node_state]
        elif node_state in visited:
            continue
        visited.add(node_state)
        for cost, neighbor_position, direction in neighbors_for_node(
            graph, node_position, node_direction, move_range
        ):
            neighbor_state = (neighbor_position, direction)
            if neighbor_state in visited:
                continue
            new_cost = cost + shortest[node_state]
            if neighbor_state not in shortest or new_cost < shortest[neighbor_state]:
                shortest[neighbor_state] = new_cost
            unvisited.put((new_cost, neighbor_position, direction))
    raise Exception("Hm....")


def parse_input(input_path: Path):
    return tuple(tuple(map(int, row)) for row in input_path.read_text().splitlines())


def solve_part_one(input_path: Path):
    city_map = parse_input(input_path)
    height = len(city_map)
    width = len(city_map[0])

    start = Position(0, 0)
    goal = Position(width - 1, height - 1)

    cost = dijkstras_algorithm(city_map, start, goal)
    return cost


def solve_part_two(input_path: Path):
    city_map = parse_input(input_path)
    height = len(city_map)
    width = len(city_map[0])

    start = Position(0, 0)
    goal = Position(width - 1, height - 1)

    cost = dijkstras_algorithm(city_map, start, goal, move_range=(4, 10))
    return cost


if __name__ == "__main__":
    main()
