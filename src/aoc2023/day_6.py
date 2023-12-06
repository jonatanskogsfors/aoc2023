import re
from functools import reduce
from pathlib import Path


def main():
    input_path = Path("input/input_6.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))


def race(race_duration: int, button_time: int):
    return button_time * max(race_duration - button_time, 0)


def find_record_breakers(race_duration, record):
    return [
        distance
        for button_time in range(1, race_duration)
        if (distance := race(race_duration, button_time)) > record
    ]


def parse_input(input_path: Path, kern=False):
    rows = input_path.read_text().splitlines()
    number_pattern = re.compile(r"(\d+)")
    if kern:
        return tuple([int("".join(number_pattern.findall(row))) for row in rows])

    race_duration, records = [map(int, number_pattern.findall(row)) for row in rows]
    return tuple(zip(race_duration, records))


def solve_part_one(input_path: Path):
    races = parse_input(input_path)
    return reduce(
        lambda a, b: a * b,
        [len(find_record_breakers(race_time, record)) for race_time, record in races],
    )


def solve_part_two(input_path: Path):
    race_time, record = parse_input(input_path, kern=True)
    return len(find_record_breakers(race_time, record))


if __name__ == "__main__":
    main()
