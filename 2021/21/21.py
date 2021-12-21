from typing import Iterator


def parse_starting_points() -> tuple[int, int]:
    p1 = int(input().split(" ")[-1])
    p2 = int(input().split(" ")[-1])
    return p1, p2


def generate_deterministic_dice() -> Iterator[int]:
    i = 0
    while True:
        total = 0
        for _ in range(3):
            i += 1
            if i > 100:
                i = 1
            total += i
        yield total


def do_step(pos: int, move: int) -> int:
    return ((pos - 1 + move) % 10) + 1


def main1() -> int:
    pos_p1, pos_p2 = parse_starting_points()
    score_p1, score_p2 = 0, 0
    nb_rolls = 0
    dice_generator = generate_deterministic_dice()

    while True:
        pos_p1 = do_step(pos_p1, next(dice_generator))
        score_p1 += pos_p1
        nb_rolls += 3
        if score_p1 >= 1000:
            return nb_rolls * score_p2

        pos_p2 = do_step(pos_p2, next(dice_generator))
        score_p2 += pos_p2
        nb_rolls += 3

        if score_p2 >= 1000:
            return nb_rolls * score_p1


UNIVERSES_FACTOR = {
    3: 1,  # 1 + 1 + 1
    4: 3,  # 1 + 1 + 2, 1 + 2 + 1, 2 + 1 + 1,
    5: 6,  # 2 + 2 + 1, 2 + 1 + 2, 1 + 2 + 2, 1 + 1 + 3, 1 + 3 + 1, 3 + 1 + 1
    6: 7,  # 2 + 2 + 2, 1 + 2 + 3, 1 + 3 + 2, 3 + 2 + 1, 3 + 1 + 2, 2 + 3 + 1, 2 + 1 + 3
    7: 6,  # 2 + 2 + 3, 2 + 3 + 2, 3 + 2 + 2, 3 + 3 + 1, 3 + 1 + 3, 1 + 3 + 3
    8: 3,  # 3 + 3 + 2, 3 + 2 + 3, 2 + 3 + 3
    9: 1,  # 3 + 3 + 3
}


__cache: dict[tuple[int, int, int, int, bool], tuple[int, int]] = {}


def simulate_universe(
    score_p1: int, score_p2: int, pos_p1: int, pos_p2: int, is_p1_turn: bool
) -> tuple[int, int]:
    if (score_p1, score_p2, pos_p1, pos_p2, is_p1_turn) in __cache:
        return __cache[(score_p1, score_p2, pos_p1, pos_p2, is_p1_turn)]

    total_universe_p1, total_universe_p2 = 0, 0
    if score_p1 >= 21:
        return 1, 0
    elif score_p2 >= 21:
        return 0, 1

    for total_dice in UNIVERSES_FACTOR.keys():
        new_p1_pos = do_step(pos_p1, total_dice) if is_p1_turn else pos_p1
        new_p2_pos = do_step(pos_p2, total_dice) if not is_p1_turn else pos_p2
        new_score_p1 = score_p1 + (new_p1_pos if is_p1_turn else 0)
        new_score_p2 = score_p2 + (new_p2_pos if not is_p1_turn else 0)

        res = simulate_universe(
            new_score_p1,
            new_score_p2,
            new_p1_pos,
            new_p2_pos,
            is_p1_turn=not is_p1_turn,
        )
        total_universe_p1 += UNIVERSES_FACTOR[total_dice] * res[0]
        total_universe_p2 += UNIVERSES_FACTOR[total_dice] * res[1]

    __cache[(score_p1, score_p2, pos_p1, pos_p2, is_p1_turn)] = (
        total_universe_p1,
        total_universe_p2,
    )
    return total_universe_p1, total_universe_p2


def main2() -> int:
    pos_p1, pos_p2 = parse_starting_points()
    total_universe_p1, total_universe_p2 = simulate_universe(
        0, 0, pos_p1, pos_p2, is_p1_turn=True
    )
    return max(total_universe_p1, total_universe_p2)
