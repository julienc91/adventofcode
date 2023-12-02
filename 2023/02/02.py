import re
import math

from utils.parsing import parse_input
from enum import Enum


class Colors(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


def get_max_cubes_in_game(game: str) -> dict[Colors, int]:
    return {
        color: max(int(count) for count in re.findall(rf"(\d+) {color.value}", game))
        for color in Colors
    }


def main1() -> int:
    total = 0
    max_colors = {Colors.RED: 12, Colors.GREEN: 13, Colors.BLUE: 14}
    for game_id, line in enumerate(parse_input(), start=1):
        for color, count in get_max_cubes_in_game(line).items():
            if count > max_colors[color]:
                break
        else:
            total += game_id
    return total


def main2() -> int:
    return sum(
        math.prod(get_max_cubes_in_game(line).values()) for line in parse_input()
    )
