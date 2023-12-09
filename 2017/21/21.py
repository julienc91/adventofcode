import math
from collections.abc import Iterator

from utils.parsing import parse_input

Square = tuple[str, ...]


def split_square(square: Square) -> list[Square]:
    split_size = 2 if (len(square) % 2 == 0) else 3
    nb_squares_per_row = len(square) // split_size
    nb_squares = nb_squares_per_row**2
    squares = []

    for square_index in range(nb_squares):
        start_x = (square_index % nb_squares_per_row) * split_size
        start_y = (square_index // nb_squares_per_row) * split_size

        grid = []
        for y in range(start_y, start_y + split_size):
            grid.append(square[y][start_x : start_x + split_size])
        squares.append(tuple(grid))
    return squares


def merge_squares(*squares: Square) -> Square:
    nb_squares = len(squares)
    nb_squares_per_row = math.isqrt(nb_squares)
    square_size = len(squares[0])

    result = []
    for square_index in range(nb_squares):
        square = squares[square_index]
        y = (square_index // nb_squares_per_row) * square_size
        for i, row in enumerate(square):
            try:
                result[y + i] += row
            except IndexError:
                result.append(row)
    return tuple(result)


def enhance_square(square: Square, rules: dict[Square, Square]) -> Square:
    squares = split_square(square)
    return merge_squares(*(rules[square] for square in squares))


def parse_rules() -> dict[tuple[str, ...], tuple[str, ...]]:
    res = {}
    for line in parse_input():
        left, right = line.split(" => ")
        res[tuple(left.split("/"))] = tuple(right.split("/"))
    return res


def flip_square(square: Square) -> Iterator[Square]:
    yield square
    yield tuple(row[::-1] for row in square)


def rotate_square(square: Square) -> Iterator[Square]:
    yield square
    for _ in range(3):
        square = tuple("".join(row) for row in list(zip(*square[::-1])))
        yield square


def complete_rules(rules: dict[Square, Square]) -> None:
    completed_rules = {}
    for pattern, enhanced_pattern in rules.items():
        for rotation in rotate_square(pattern):
            for flip in flip_square(rotation):
                completed_rules[flip] = enhanced_pattern
    rules.update(completed_rules)


def _main(nb_iterations: int) -> int:
    square = Square((".#.", "..#", "###"))
    rules = parse_rules()
    complete_rules(rules)

    for _ in range(nb_iterations):
        square = enhance_square(square, rules)
    return sum(row.count("#") for row in square)


def main1() -> int:
    return _main(5)


def main2() -> int:
    return _main(18)
