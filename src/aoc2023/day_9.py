from itertools import pairwise
from pathlib import Path


def main():
    input_path = Path("input/input_9.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))


def derive(sequence: tuple[int, ...]):
    if set(sequence) == {0}:
        return None
    return tuple(b - a for a, b in pairwise(sequence))


def next_number(sequence: tuple[int, ...], left=False):
    if (derivative := derive(sequence)) is None:
        return 0
    end_index = left - 1
    operator = (lambda a, b: a - b) if left else (lambda a, b: a + b)
    return operator(sequence[end_index], next_number(derivative, left=left))


def parse_input(input_path: Path):
    return tuple(
        tuple(map(int, line.split())) for line in input_path.read_text().splitlines()
    )


def solve_part_one(input_path: Path):
    sequences = parse_input(input_path)
    return sum(next_number(sequence) for sequence in sequences)


def solve_part_two(input_path: Path):
    sequences = parse_input(input_path)
    return sum(next_number(sequence, left=True) for sequence in sequences)


if __name__ == "__main__":
    main()
