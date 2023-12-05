import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple, Self


def main():
    input_path = Path("input/input_5.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))


@dataclass
class CategoryRange:
    destination: int
    source: int
    length: int

    @property
    def destination_end(self) -> int:
        return self.destination + self.length - 1

    @property
    def source_end(self) -> int:
        return self.source + self.length - 1

    def __hash__(self):
        return hash((self.destination, self.source, self.length))


def split_ranges(
    left_range: CategoryRange, right_range: CategoryRange
) -> list[CategoryRange]:
    left_start_inside_right = (
        right_range.source <= left_range.destination <= right_range.source_end
    )
    left_end_inside_right = (
        right_range.source <= left_range.destination_end <= right_range.source_end
    )
    ranges_overlap = left_start_inside_right or left_end_inside_right

    if not ranges_overlap:
        return None

    a_length = abs(right_range.source - left_range.destination)
    b_length = (
        min(left_range.destination_end, right_range.source_end)
        - max(right_range.source, left_range.destination)
        + 1
    )
    c_length = abs(right_range.source_end - left_range.destination_end)

    if left_range.destination < right_range.source:
        # Left, no overlap
        a_source = left_range.source
        a_destination = left_range.destination

        # Middle, overlap
        b_source = left_range.source + a_length
        b_destination = right_range.destination

    elif left_range.destination >= right_range.source:
        a_source = right_range.source
        a_destination = right_range.destination

        # Middle, overlap
        b_source = right_range.source + a_length
        b_destination = right_range.destination + a_length
    else:
        raise Exception("OOPS")

    if left_range.destination_end < right_range.source_end:
        c_source = right_range.source_end - c_length + 1
        c_destination = right_range.destination + b_length

    elif left_range.destination_end >= right_range.source_end:
        c_source = left_range.source + b_length
        c_destination = right_range.source_end + 1
    else:
        raise Exception("OOPS")

    new_ranges = [CategoryRange(b_destination, b_source, b_length)]
    if a_length:
        new_ranges.append(CategoryRange(a_destination, a_source, a_length))

    if c_length:
        new_ranges.append(CategoryRange(c_destination, c_source, c_length))

    return new_ranges


@dataclass
class SeedRange:
    start: int
    length: int

    @property
    def end(self) -> int:
        return self.start + self.length - 1

    def __hash__(self):
        return hash((self.start, self.length))


class CategoryMap:
    def __init__(self, *map_ranges: CategoryRange):
        self._map_ranges = list(map_ranges)

    def convert(self, source: int):
        for map_range in self._map_ranges:
            if map_range.source <= source < map_range.source + map_range.length:
                difference = source - map_range.source
                # print(f"{source} -> {map_range.destination + difference}")
                return map_range.destination + difference
        # print(f"{source} -> {source}")
        return source

    def combine(self, other_map: Self):
        combined_ranges = []
        unchecked_ranges = other_map._map_ranges
        while unchecked_ranges:
            unchecked_range = unchecked_ranges.pop()
            range_split = False
            for map_range in self._map_ranges:
                if new_ranges := split_ranges(map_range, unchecked_range):
                    unchecked_ranges += new_ranges
                    range_split = True
                    self._map_ranges.remove(map_range)
                    break
            if not range_split:
                combined_ranges.append(unchecked_range)

        self._map_ranges = combined_ranges


def parse_input(input_path: Path):
    raw_input = input_path.read_text()
    seed_input, categories_input = raw_input.split("\n", 1)
    seeds = map(int, seed_input.split(":")[1].strip().split())
    category_map = None
    for category in categories_input.strip().split("\n\n"):
        header, *ranges = category.split("\n")
        new_map = CategoryMap(
            *[CategoryRange(*map(int, range.split())) for range in ranges]
        )
        if category_map is None:
            category_map = new_map
        else:
            category_map.combine(new_map)
    return seeds, category_map


def seeds_to_ranges(seeds):
    return [SeedRange(start, length) for start, length in itertools.batched(seeds, 2)]


def solve_part_one(input_path):
    seeds, category_map = parse_input(input_path)
    corresponding_numbers = []
    for seed in seeds:
        location = category_map.convert(seed)
        corresponding_numbers.append(location)
    return min(corresponding_numbers)


def solve_part_two(input_path):
    seeds, category_map = parse_input(input_path)
    seed_ranges = seeds_to_ranges(seeds)
    corresponding_numbers = []
    for seed_range in seed_ranges:
        print(seed_range.length)
        for seed in range(seed_range.start, seed_range.start + seed_range.length):
            location = category_map.convert(seed)
            corresponding_numbers.append(location)
    return min(corresponding_numbers)


if __name__ == "__main__":
    main()
