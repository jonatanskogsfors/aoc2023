import dataclasses
import enum

from aoc2023.position import Position


class Direction(enum.Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def delta(self):
        match self.value:
            case 0:
                direction_delta = Position(1, 0)
            case 1:
                direction_delta = Position(0, 1)
            case 2:
                direction_delta = Position(-1, 0)
            case 3:
                direction_delta = Position(0, -1)
        return direction_delta
