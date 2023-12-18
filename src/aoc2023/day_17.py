import queue
from pathlib import Path

from aoc2023.direction import Direction
from aoc2023.position import Position


def main():
    input_path = Path("input/input_17.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))


def neighbors_for_node(graph, node: Position, direction: Direction):
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
    for new_direction in new_directions:
        nodes_in_direction = [
            node_in_direction
            for n in range(1, 4)
            if 0 <= (node_in_direction := node + new_direction.delta() * n).x < width
            and 0 <= node_in_direction.y < height
        ]
        for n in range(1, len(nodes_in_direction) + 1):
            cost = sum(index_graph(graph, apa) for apa in nodes_in_direction[:n])
            neighbors.add((cost, node + new_direction.delta() * n, new_direction))

    return sorted(neighbors)


def index_graph(graph, position: Position):
    return graph[position.y][position.x]


def dijkstras_algorithm(graph, start: Position, goal: Position):
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
        for cost, neighbor_position, direction in neighbors_for_node(graph, *node_state):
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
    ...


if __name__ == "__main__":
    main()
