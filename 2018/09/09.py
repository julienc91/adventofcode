import re
from collections import deque


def parse_input() -> tuple[int, int]:
    line = input()
    nb_players, last_marble = re.findall(r"\d+", line)
    return int(nb_players), int(last_marble)


def run_game(nb_players: int, last_marble: int) -> int:
    scores = [0] * nb_players
    marbles = range(3, last_marble + 1)

    circle = deque([0, 2, 1])
    current_player = 3

    for value in marbles:
        if value % 23 != 0:
            circle.append(value)
            circle.rotate(-1)
        else:
            scores[current_player] += value
            circle.rotate(8)
            scores[current_player] += circle.pop()
            circle.rotate(-2)

        current_player = (current_player + 1) % nb_players
    return max(scores)


def main1() -> int:
    nb_players, last_marble = parse_input()
    return run_game(nb_players, last_marble)


def main2() -> int:
    nb_players, n = parse_input()
    return run_game(nb_players, n * 100)
