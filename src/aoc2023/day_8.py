import math
import re
from enum import IntEnum
from itertools import cycle
from pathlib import Path


def main():
    input_path = Path("input/input_8.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))  # 109772689092430810730873 (high)


class Instruction(IntEnum):
    L = 0
    R = 1


def parse_input(input_path: Path):
    network_pattern = re.compile(r"(\w{3}) = \((\w{3}), (\w{3})\)")
    raw_instructions, raw_network = input_path.read_text().split("\n\n")

    instructions = tuple([Instruction[instruction] for instruction in raw_instructions])
    network = {
        match.group(1): (match.group(2), match.group(3))
        for match in network_pattern.finditer(raw_network)
    }

    return instructions, network


def find_cycle(start_node: str, instructions: tuple[Instruction, ...], network: dict):
    before_cycle = None
    end_node_end = "Z"
    current_node = start_node
    for steps, instruction in enumerate(cycle(instructions)):
        if current_node.endswith(end_node_end):
            if before_cycle is None:
                before_cycle = steps
            else:
                period = steps - before_cycle
                return before_cycle, period
        current_node = network[current_node][instruction]


def solve_part_one(input_path: Path):
    instructions, network = parse_input(input_path)
    current_node = "AAA"
    end_node = "ZZZ"

    for steps, instruction in enumerate(cycle(instructions)):
        if current_node == end_node:
            return steps
        current_node = network[current_node][instruction]


def solve_part_two(input_path: Path):
    instructions, network = parse_input(input_path)
    current_nodes = tuple(node for node in network if node.endswith("A"))
    periods = [find_cycle(node, instructions, network) for node in current_nodes]

    # The solution assumes that the number of steps before the cycle is equal to the
    # actual period of the cycle. Although I'm relieved that I didn't have to implement
    # LCM with offsets, I think that it is a bit too convenient from how the puzzle was
    # presented.
    assert all(start == period for start, period in periods)

    return math.lcm(*[period for _, period in periods])


if __name__ == "__main__":
    main()
