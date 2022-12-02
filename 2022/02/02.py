from enum import Enum


class Shape(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    @property
    def base_point(self) -> int:
        return self.value + 1

    @property
    def wins_against(self) -> "Shape":
        return Shape((self.value - 1) % 3)  # Props to @Atlante45!

    @property
    def loses_against(self) -> "Shape":
        return Shape((self.value + 1) % 3)

    def is_winner(self, opponent: "Shape") -> bool:
        return self.wins_against == opponent


class AbstractGame:
    def __init__(self, player: str, opponent: str):
        self.player, self.opponent = self.get_shapes(player, opponent)

    def get_score(self) -> int:
        score = self.player.base_point
        if self.player == self.opponent:
            score += 3
        elif self.player.is_winner(self.opponent):
            score += 6
        return score

    @staticmethod
    def get_shapes(player: str, opponent: str) -> tuple["Shape", "Shape"]:
        raise NotImplementedError


class Game1(AbstractGame):
    @staticmethod
    def get_shapes(player: str, opponent: str) -> tuple["Shape", "Shape"]:
        opponent_shape = {"A": Shape.ROCK, "B": Shape.PAPER, "C": Shape.SCISSORS}[
            opponent
        ]
        player_shape = {"X": Shape.ROCK, "Y": Shape.PAPER, "Z": Shape.SCISSORS}[player]
        return player_shape, opponent_shape


class Game2(AbstractGame):
    @staticmethod
    def get_shapes(player: str, opponent: str) -> tuple["Shape", "Shape"]:
        opponent_shape = {"A": Shape.ROCK, "B": Shape.PAPER, "C": Shape.SCISSORS}[
            opponent
        ]
        player_shape = {
            "X": opponent_shape.wins_against,
            "Y": opponent_shape,
            "Z": opponent_shape.loses_against,
        }[player]
        return player_shape, opponent_shape


def _main(game_type: type[AbstractGame]) -> int:
    score = 0
    try:
        while line := input().strip():
            opponent, player = line.split()
            game = game_type(player, opponent)
            score += game.get_score()
    except EOFError:
        pass
    return score


def main1() -> int:
    return _main(Game1)


def main2() -> int:
    return _main(Game2)
