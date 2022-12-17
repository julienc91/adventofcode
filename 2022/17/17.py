import itertools
from collections import defaultdict
from collections.abc import Iterator
from enum import Enum


class AbstractPiece:
    pixels: list[tuple[int, int]]


class HorizontalBar(AbstractPiece):
    pixels = [(0, 0), (1, 0), (2, 0), (3, 0)]


class Cross(AbstractPiece):
    pixels = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]


class ReverseL(AbstractPiece):
    pixels = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]


class VerticalBar(AbstractPiece):
    pixels = [(0, 0), (0, 1), (0, 2), (0, 3)]


class Square(AbstractPiece):
    pixels = [(0, 0), (1, 0), (0, 1), (1, 1)]


class JetPattern(Enum):
    LEFT = "<"
    RIGHT = ">"

    def apply(self, x: int, y: int) -> tuple[int, int]:
        if self == JetPattern.LEFT:
            return x - 1, y
        return x + 1, y


class Game:
    pieces: Iterator[type[AbstractPiece]]
    jet_patterns: Iterator[JetPattern]
    width = 7
    start_x_offset = 2
    start_y_offset = 3

    def __init__(
        self, pieces: list[type[AbstractPiece]], jet_patterns: list[JetPattern]
    ) -> None:
        self.pieces = itertools.cycle(pieces)
        self.jet_patterns = itertools.cycle(jet_patterns)
        self.grid: dict[tuple[int, int], bool] = defaultdict(bool)
        self.height = 0

    def add_piece(self) -> None:
        piece = next(self.pieces)
        start_x = self.start_x_offset
        start_y = self.height + self.start_y_offset

        pixels = [(x + start_x, y + start_y) for (x, y) in piece.pixels]
        while True:
            # Apply jet stream
            direction = next(self.jet_patterns)
            new_pixels: list[tuple[int, int]] = []
            for x, y in pixels:
                x, y = direction.apply(x, y)
                if x < 0 or self.grid[(x, y)] or x >= self.width:
                    new_pixels = pixels
                    break
                new_pixels.append((x, y))

            # Apply gravity
            pixels, new_pixels = new_pixels, []
            for x, y in pixels:
                y -= 1
                if y < 0 or self.grid[(x, y)]:
                    new_pixels = pixels
                    break
                new_pixels.append((x, y))

            # Freeze piece
            if new_pixels == pixels:
                max_y = 0
                for x, y in new_pixels:
                    max_y = max(max_y, y)
                    self.grid[(x, y)] = True
                self.height = max(self.height, max_y + 1)
                break

            pixels = new_pixels

    def run_n_times(self, n: int) -> None:
        for _ in range(n):
            self.add_piece()


def main1() -> int:
    pieces = [HorizontalBar, Cross, ReverseL, VerticalBar, Square]
    jet_patterns = [JetPattern(char) for char in input().strip()]
    game = Game(pieces=pieces, jet_patterns=jet_patterns)
    game.run_n_times(2022)
    return game.height


def get_loop_details(cycle_heights: list[int]) -> tuple[int, int]:
    loop_length = 1
    cycle_heights = cycle_heights[::-1]
    while True:
        reference_loop_height = sum(cycle_heights[:loop_length])
        for i in range(1, 5):
            loop_height = sum(cycle_heights[loop_length * i : loop_length * (i + 1)])
            if loop_height == 0:
                raise RuntimeError()
            if loop_height != reference_loop_height:
                loop_length += 1
                break
        else:
            return loop_length, reference_loop_height


def get_offset_details(
    cycle_heights: list[int], loop_length: int, loop_height: int
) -> tuple[int, int]:
    cycle_heights = cycle_heights
    offset = 0
    while True:
        current_loop_height = sum(cycle_heights[offset : offset + loop_length])
        if current_loop_height != loop_height:
            offset += 1
            continue

        return offset, sum(cycle_heights[:offset])


def main2() -> int:
    pieces = [HorizontalBar, Cross, ReverseL, VerticalBar, Square]
    jet_patterns = [JetPattern(char) for char in input().strip()]

    game = Game(pieces=pieces, jet_patterns=jet_patterns)
    nb_pieces = len(pieces)

    # Record the height added everytime all the pieces are added to the game once on the first X cycles
    cycle_heights: list[int] = []
    last_height = 0
    for _ in range(10000):
        game.run_n_times(nb_pieces)
        height = game.height
        cycle_heights.append(height - last_height)
        last_height = height

    # From this list of heights, we should be able to find a loop pattern
    loop_length, loop_height = get_loop_details(cycle_heights)

    # And with the characteristics of this loop, we can now determine exactly when it appears,
    # and thus determine the characterstics of the first games (called "offset" here)
    offset_length, offset_height = get_offset_details(
        cycle_heights, loop_length, loop_height
    )

    loop_length *= nb_pieces
    offset_length *= nb_pieces

    nb_runs = 1_000_000_000_000
    nb_loops = (nb_runs - offset_length) // loop_length
    remaining_length = (nb_runs - offset_length) % loop_length

    # We only need to retrieve the height of the final few rounds, which do not constitute a complete loop
    game = Game(pieces=pieces, jet_patterns=jet_patterns)
    game.run_n_times(offset_length + remaining_length)
    remaining_height = game.height - offset_height

    # The result is the sum of:
    # - the height of the offset
    # - n times the height of the loop
    # - the height of the reminder
    return offset_height + nb_loops * loop_height + remaining_height
