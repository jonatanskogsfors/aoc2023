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

    def __add__(self, other):
        if isinstance(other, Position):
            return Position(self.x + other.x, self.y + other.y)
        raise NotImplementedError()

    def __sub__(self, other):
        if isinstance(other, Position):
            return Position(self.x - other.x, self.y - other.y)
        raise NotImplementedError()

    def __mul__(self, other):
        if isinstance(other, int):
            return Position(self.x * other, self.y * other)
        raise NotImplementedError()

    def __lt__(self, other):
        return (self.x + self.y) < (other.x + other.y)


@dataclasses.dataclass
class Position3d(Position):
    z: int = 0
