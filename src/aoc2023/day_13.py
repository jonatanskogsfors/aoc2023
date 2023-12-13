import enum
import itertools
import math
from pathlib import Path


def main():
    input_path = Path("input/input_13.txt")
    print(solve_part_one(input_path))  # 27441 (low),
    print(solve_part_two(input_path))


class Axis(enum.Enum):
    HORIZONTAL = 0
    VERTICAL = 1


def parse_input(input_path: Path):
    return tuple(
        [tuple(pattern.splitlines()) for pattern in input_path.read_text().split("\n\n")]
    )


def row_as_number(row: str) -> int:
    return int(row.replace("#", "1").replace(".", "0"), 2)


def find_mirror(pattern: tuple[str, ...], fix_smudges: bool = False):
    rows = [row_as_number(row) for row in pattern]
    columns = [
        row_as_number("".join([row[n] for row in pattern]))
        for n in range(len(pattern[0]))
    ]

    (best_horizontal, horizontal_position), *_ = best_mirror_position_for_axis(
        rows, fix_smudges=fix_smudges
    )
    (best_vertical, vertical_position), *_ = best_mirror_position_for_axis(
        columns, fix_smudges=fix_smudges
    )

    if best_vertical > best_horizontal:
        return Axis.VERTICAL, vertical_position
    else:
        return Axis.HORIZONTAL, horizontal_position


def rows_are_equal(a: int, b: int, fix_smudges: bool = False):
    if not fix_smudges or a == b:
        return a == b, False

    bits = math.ceil((math.log2(max(a, b))))
    for n in range(bits):
        bit_flip_mask = ["0"] * bits
        bit_flip_mask[n] = "1"
        bit_flip_mask = int("".join(bit_flip_mask), 2)

        if a ^ bit_flip_mask == b:
            return True, True
    return False, False


def best_mirror_position_for_axis(rows, fix_smudges: bool = False):
    positions = []
    for n, (a, b) in enumerate(itertools.pairwise(rows)):
        if not rows_are_equal(a, b, fix_smudges=fix_smudges)[0]:
            continue

        mirror_position = n + 1
        row_equality = [
            rows_are_equal(a, b, fix_smudges=fix_smudges)
            for a, b in zip(reversed(rows[:mirror_position]), rows[mirror_position:])
        ]

        if (
            all(equality for equality, _ in row_equality)
            and sum(fixed for _, fixed in row_equality) == fix_smudges
        ):
            positions.append((abs(mirror_position - len(rows)), mirror_position))
    if not positions:
        positions.append((0, 0))
    return sorted(positions)


def solve_part_one(input_path: Path):
    patterns = parse_input(input_path)
    mirrors = [find_mirror(pattern) for pattern in patterns]
    return sum(
        mirror[1] * (100 if mirror[0] == Axis.HORIZONTAL else 1) for mirror in mirrors
    )


def solve_part_two(input_path: Path):
    patterns = parse_input(input_path)
    mirrors = [find_mirror(pattern, fix_smudges=True) for pattern in patterns]
    return sum(
        mirror[1] * (100 if mirror[0] == Axis.HORIZONTAL else 1) for mirror in mirrors
    )


if __name__ == "__main__":
    main()
