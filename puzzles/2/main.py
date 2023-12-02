import re
from functools import reduce
from pathlib import Path
from typing import Dict, List

from puzzles.util import read_file_into_list


def parse_game_as_dict(game: str) -> Dict:
    """
    Parse string representing game results into nested dict with key as game ID.

    Args:
        game (str): Game outcomes e.g. "Game 1: 1 red, 5 blue; 5 green, 6 blue, 12 red"
    Returns:
        Dict: Nested dictionary with key for game ID e.g. {1: {1: {"red": 1, "blue": 5},
            2: {"red": 12, "blue": 6, "green": 5}}}.
    """
    # identify ID number
    pattern = r"Game (\d+):"
    game_id = re.search(pattern, game).group(1)

    # split up into reveals
    reveals = [r.strip().split(", ") for r in game.split(":")[1].split(";")]

    # create dict of results
    results = {}
    for number, reveal in enumerate(reveals, start=1):
        results[number] = {
            colour: int(count) for r in reveal for count, colour in [r.split(" ")]
        }

    return {int(game_id): results}


def is_valid_reveal(config: Dict, reveal: Dict) -> bool:
    """
    Check if reveal is allowed based on input config.

    Args:
        config (Dict): Input configuration for red, blue and green cubes.
        reveal (Dict): Counts of coloured cubes e.g. {"green": 10, "red": 5}.
    Returns:
        bool: True if the counts are within range as set by config.
    """
    return all(count <= config.get(colour, 0) for colour, count in reveal.items())


def get_sum_of_possible_games(config: Dict, games: Dict) -> int:
    """
    Total sum of possible games (using game ID) based on input configuration.

    Args:
        config (Dict): Input configuration for red, blue and green cubes.
        games (Dict): Game results.
    Returns:
        int: Sum of games.
    """
    return sum(
        game_id
        for game_id, results in games.items()
        # include game ID if all reveals for a game are valid
        if all(is_valid_reveal(config, reveal) for reveal in results.values())
    )


def get_minimum_cubes(game: Dict) -> List:
    """
    Get minimum cubes required per colour for game.
    Example input for Game 1:
    {1: {"blue": 3, "red" : 4}, 2: {"red": 1, "green": 2, "blue": 6}, 3: {"green": 2}}
    Returns: [4, 2, 6]

    Args:
        game (Dict): Reveals for a game.
    Returns:
        List: Minimum cubes required for each colour.
    """
    minimum = {"red": 1, "green": 1, "blue": 1}
    for reveal in game.values():
        for colour, count in reveal.items():
            minimum[colour] = max(minimum.get(colour), count)
    return list(minimum.values())


def get_sum_of_set_powers(games: Dict) -> int:
    """
    Power of a set of cubes is equal to the numbers of red, green, and blue cubes
    multiplied together. Take the total sum across all games.
    Args:
        games (Dict): Game results.
    Returns:
        int: Total sum of the set of powers for each game.
    """
    return sum(
        reduce(lambda x, y: x * y, get_minimum_cubes(game)) for game in games.values()
    )


def main():
    # read input file
    data = read_file_into_list(Path(__file__).parent / "input.txt")

    # create dict of game results
    games = {}
    for game in data:
        games.update(parse_game_as_dict(game))

    # sum of games where possible
    configuration = {"red": 12, "green": 13, "blue": 14}
    sum_of_possible_games = get_sum_of_possible_games(configuration, games)
    print(
        f"Sum of games where reveals would have been possible: {sum_of_possible_games}"
    )

    # sum of the power of cube sets
    sum_of_set_powers = get_sum_of_set_powers(games)
    print(f"Sum of cube set powers: {sum_of_set_powers}")


if __name__ == "__main__":
    main()
