import dataclasses
from typing import Self


@dataclasses.dataclass
class Position:
    x: int = 0
    y: int = 0

    def __hash__(self):
        return hash((self.x, self.y))

    def manhattan(self, other: Self):
        return abs(self.x - other.x) + abs(self.y - other.y)