from pathlib import Path

NUMBERS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def parse_input(path: Path):
    return path.read_text().strip("\n").split("\n")


def decode_calibration(row: str, allow_words=False) -> int:
    return int(first_number(row, allow_words) + last_number(row, allow_words))


def first_number(row, allow_words=False) -> str:
    for n in range(len(row)):
        for name, value in NUMBERS.items():
            substring = row[: n + 1]
            if str(value) in substring:
                return str(value)
            if allow_words and name in substring:
                return str(value)
    return None


def last_number(row, allow_words=False):
    for n in range(len(row)):
        for name, value in NUMBERS.items():
            substring = row[-(n + 1) :]
            if str(value) in substring:
                return str(value)
            if allow_words and name in substring:
                return str(value)
    return None


def solve_part_one(input_path: Path) -> int:
    parsed_input = parse_input(input_path)
    numbers = [decode_calibration(row) for row in parsed_input]
    return sum(numbers)


def solve_part_two(input_path: Path) -> int:
    parsed_input = parse_input(input_path)
    numbers = [decode_calibration(row, allow_words=True) for row in parsed_input]
    return sum(numbers)


if __name__ == "__main__":
    input_path = Path("input/input_1.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))  # 53363 -> 53343 -> _53340_
