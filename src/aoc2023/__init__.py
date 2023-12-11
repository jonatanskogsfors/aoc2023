from pathlib import Path

__all__ = [module.stem for module in Path(__file__).parent.glob("day_*.py")]

from aoc2023 import *
