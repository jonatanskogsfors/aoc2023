import functools
import re
from pathlib import Path


def main():
    input_path = Path("input/input_12.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))


@functools.cache
def matches(group: str, substring: str):
    return bool(re.match(substring.replace(".", r"\.").replace("?", "."), group))


@functools.cache
def arrangements_for_row(row, groups):
    all_arrangements = 0
    more_than_one = 2
    last_group = len(groups) < more_than_one

    if last_group:
        first_group = groups[0]
        other_groups = ()
    else:
        first_group, *other_groups = groups

    last_possible = len(row) - (sum(groups) + len(groups) - 1) + 1
    if "#" in row:
        last_possible = min(last_possible, row.find("#") + 2)
    for n in range(last_possible):
        group_string = "." * n + "#" * first_group
        if last_group:
            group_string += "." * (len(row) - len(group_string))
        else:
            group_string += "."

        substring, rest_of_row = row[: len(group_string)], row[len(group_string) :]
        if not matches(group_string, substring):
            continue
        if other_groups:
            all_arrangements += arrangements_for_row(rest_of_row, tuple(other_groups))
        else:
            all_arrangements += 1
    return all_arrangements


def parse_input(input_path: Path):
    return [
        (row, tuple(map(int, groups.split(","))))
        for row, groups in [
            record.split(" ") for record in input_path.read_text().splitlines()
        ]
    ]


def unfold_record(row: str, groups: tuple[int, ...]):
    return "?".join([row] * 5), groups * 5


def solve_part_one(input_path: Path):
    records = parse_input(input_path)
    all_arrangements = [arrangements_for_row(row, groups) for row, groups in records]
    return sum(all_arrangements)


def solve_part_two(input_path: Path):
    records = parse_input(input_path)
    records = [unfold_record(row, groups) for row, groups in records]
    all_arrangements = [arrangements_for_row(row, groups) for row, groups in records]
    return sum(all_arrangements)


if __name__ == "__main__":
    main()
