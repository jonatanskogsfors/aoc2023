import re
from collections import defaultdict
from functools import reduce
from pathlib import Path

GAME_HEADER_PATTERN = re.compile(r"Game (\d+)")


def main():
    input_path = Path("input/input_2.txt")
    print(solve_part_one(input_path))
    print(solve_part_two(input_path))


def parse_input(input_path: Path):
    game_rows = input_path.read_text().strip().split("\n")
    games = {}
    for game_row in game_rows:
        game_header, game = game_row.split(":")
        if games_header_match := GAME_HEADER_PATTERN.match(game_header):
            game_id = int(games_header_match.group(1))
            games[game_id] = game.strip()
    return games


def is_game_possible(game: str, rule: dict) -> bool:
    total_colors = max_by_color(game)
    return all(items <= rule[color] for color, items in total_colors.items())


def max_by_color(game: str) -> dict:
    max_colors = defaultdict(int)
    for subset in game.split(";"):
        for color_cubes in subset.strip().split(","):
            cubes, color = color_cubes.strip().split(" ")
            color = color.lower()
            cubes = int(cubes)
            max_colors[color] = max(cubes, max_colors[color])
    return max_colors


def solve_part_one(input_path: Path) -> int:
    parsed_games = parse_input(input_path)
    rule = {"red": 12, "green": 13, "blue": 14}
    possible_games = [
        game_id for game_id, game in parsed_games.items() if is_game_possible(game, rule)
    ]
    return sum(possible_games)


def solve_part_two(input_path: Path) -> int:
    parsed_games = parse_input(input_path)
    powers = [
        reduce(lambda a, b: a * b, max_by_color(game).values())
        for game in parsed_games.values()
    ]

    return sum(powers)


if __name__ == "__main__":
    main()
