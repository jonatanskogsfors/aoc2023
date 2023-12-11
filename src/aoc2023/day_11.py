from itertools import combinations
from pathlib import Path

from aoc2023.position import Position


def main():
    input_path = Path("input/input_11.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))


class AstronomicalImage:
    def __init__(self, image_data):
        self._image_data = image_data
        self._expansion_factor = 1

    @property
    def rows(self):
        return iter(self._image_data)

    @property
    def columns(self):
        for n in range(len(self._image_data[0])):
            yield "".join(row[n] for row in self._image_data)

    def expand(self, factor: int = 2):
        self._expansion_factor = factor

    def stars(self):
        expanded_stars = set()

        x_pansions = {}
        for n, column in enumerate(self.columns):
            if set(column) == {"."}:
                x_pansions[n] = (self._expansion_factor - 1) * (len(x_pansions) + 1)

        y_pansion = 0
        for y, row in enumerate(self.rows):
            if set(row) == {"."}:
                y_pansion += self._expansion_factor - 1
            else:
                for x, char in enumerate(row):
                    if char == "#":
                        if previous_x_pansions := [key for key in x_pansions if key < x]:
                            x_pansion = x_pansions[max(previous_x_pansions)]
                        else:
                            x_pansion = 0
                        expanded_stars.add(Position(x + x_pansion, y + y_pansion))
        return expanded_stars


def parse_data(input_path: Path):
    return tuple(input_path.read_text().splitlines())


def solve_part_one(input_path: Path):
    image_data = parse_data(input_path)
    image = AstronomicalImage(image_data)
    image.expand()
    return sum(a.manhattan(b) for a, b in combinations(image.stars(), 2))


def solve_part_two(input_path: Path, expansion_factor: int = 1_000_000):
    image_data = parse_data(input_path)
    image = AstronomicalImage(image_data)
    image.expand(expansion_factor)
    return sum(a.manhattan(b) for a, b in combinations(image.stars(), 2))


if __name__ == "__main__":
    main()
