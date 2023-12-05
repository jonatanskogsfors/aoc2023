from pathlib import Path
from typing import NamedTuple


class CategoryRange(NamedTuple):
    destination: int
    source: int
    length: int


class CategoryMap:
    def __init__(self, *map_ranges: CategoryRange):
        self._map_ranges = map_ranges

    def convert(self, source: int) -> int:
        for map_range in self._map_ranges:
            if map_range.source <= source <= map_range.source + map_range.length:
                difference = source - map_range.source
                return map_range.destination + difference
        return source

def parse_input(input_path: Path):
    raw_input = input_path.read_text()
    seed_input_categories_input = raw_input.split("\n", 1)
    seeds = map(
        int, seed_input.split(":")[1].strip().split()
    )
    for category in

