from pathlib import Path

NUMBERS = {
    "zero": 0,
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


def decode_row(row: str, only_true_digits = False) -> int:
    buffer = ""
    numbers = []
    for character in row:
        if character.isdigit():
            numbers += _numbers_in_buffer(buffer)
            buffer = ""
            numbers.append(character)

        elif not only_true_digits:
            buffer += character
    numbers += _numbers_in_buffer(buffer)
    return int(numbers[0] + numbers[-1])


def _numbers_in_buffer(buffer: str) -> list[str]:
    found_numbers = []
    for name, value in NUMBERS.items():
        position = buffer.find(name)
        if position != -1:
            found_numbers.append((position, value))
    return [str(value) for _, value in sorted(found_numbers)]


def solve_part_one(input_path: Path) -> int:
    parsed_input = parse_input(input_path)
    numbers = [decode_row(row, True) for row in parsed_input]
    return sum(numbers)

def solve_part_two(input_path: Path) -> int:
    parsed_input = parse_input(input_path)
    numbers = [decode_row(row) for row in parsed_input]
    return sum(numbers)

#53363 High
#53343 High
print(solve_part_one(Path("1/input.txt")))
print(solve_part_two(Path("1/input.txt")))

for row in parse_input(Path("1/input.txt")):
    print(f"{decode_row(row)}: {row}")