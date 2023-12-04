import re
from pathlib import Path
from typing import NamedTuple

NUMBER_PATTERN = re.compile(r"(\d+)")


class ItemPosition(NamedTuple):
    value: int | str
    x: int
    y: int


def main():
    input_path = Path("input/input_3.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))


def parse_input(input_path: Path) -> tuple[str]:
    return tuple(input_path.read_text().strip().split("\n"))


def adjacent_indices(given_number: ItemPosition):
    number_width = len(str(given_number.value))
    row_above = {
        (x, given_number.y - 1)
        for x in range(given_number.x - 1, given_number.x + number_width + 1)
    }

    same_row = {
        (given_number.x - 1, given_number.y),
        (given_number.x + number_width, given_number.y),
    }

    row_below = {
        (x, given_number.y + 1)
        for x in range(given_number.x - 1, given_number.x + number_width + 1)
    }

    adjacent = row_above | same_row | row_below
    return {(x, y) for x, y in adjacent if x >= 0 and y >= 0}


def adjacent_symbol(number, schematic):
    for x, y in adjacent_indices(number):
        try:
            character = schematic[y][x]
        except IndexError:
            continue
        if character not in "0123456789.":
            return ItemPosition(character, x, y)
    return None


def numbers_in_schematic(schematic: tuple[str]):
    numbers = set()
    for y, row in enumerate(schematic):
        for number_match in NUMBER_PATTERN.finditer(row):
            value = int(number_match.group(1))
            numbers.add(ItemPosition(value, number_match.start(), y))
    return numbers


def cogs_in_schematics(schematic):
    numbers = numbers_in_schematic(schematic)

    cog_candidates = {}
    cogs = set()
    for number in numbers:
        symbol = adjacent_symbol(number, schematic)
        if symbol and symbol.value == "*":
            if symbol in cog_candidates:
                gear_ratio = number.value * cog_candidates[symbol].value
                cogs.add(ItemPosition(gear_ratio, symbol.x, symbol.y))
            else:
                cog_candidates[symbol] = number
    return cogs


def solve_part_one(input_path: Path):
    schematic = parse_input(input_path)
    numbers = numbers_in_schematic(schematic)
    parts = [number.value for number in numbers if adjacent_symbol(number, schematic)]
    return sum(parts)


def solve_part_two(input_path: Path):
    schematic = parse_input(input_path)
    cogs = cogs_in_schematics(schematic)
    return sum(cog.value for cog in cogs)

    return 0


if __name__ == "__main__":
    main()
