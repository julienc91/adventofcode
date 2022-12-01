import math
from ast import literal_eval

Number = int | list["Number"]


def parse_input() -> list[Number]:
    res = []
    try:
        while line := input().strip():
            number = literal_eval(line)
            res.append(number)
    except EOFError:
        pass
    return res


def add_carry(n: Number, carry: int, left: bool) -> Number:
    match n:
        case int():
            return n + carry
        case [a, b]:
            if left:
                return [add_carry(a, carry, left), b]
            else:
                return [a, add_carry(b, carry, left)]
        case _:
            raise ValueError()


def explode(n: Number) -> tuple[bool, Number]:
    def explode_(n_: Number, depth: int) -> tuple[bool, Number, int, int]:
        match n_:
            case int():
                return False, n, 0, 0
            case [a, b]:
                if depth >= 4:
                    return True, 0, a, b

                has_exploded, new_a, left, right = explode_(a, depth + 1)
                if has_exploded:
                    if right > 0:
                        b = add_carry(b, right, True)
                    return True, [new_a, b], left, 0

                has_exploded, new_b, left, right = explode_(b, depth + 1)
                if has_exploded:
                    if left > 0:
                        a = add_carry(a, left, False)
                    return True, [a, new_b], 0, right
                return False, [a, b], 0, 0

    exploded, res, _, _ = explode_(n, 0)
    return exploded, res


def split(n: Number) -> tuple[bool, Number]:
    if isinstance(n, int):
        if n >= 10:
            return True, [math.floor(n / 2), math.ceil(n / 2)]
        else:
            return False, n
    a, b = n

    split_left, a = split(a)
    if split_left:
        return True, [a, b]
    split_right, b = split(b)
    if split_right:
        return True, [a, b]
    return False, [a, b]


def add(a: Number, b: Number) -> Number:
    res = [a, b]
    while True:
        has_exploded, res = explode(res)
        if has_exploded:
            continue

        has_splitted, res = split(res)
        if has_splitted:
            continue

        return res


def magnitude(n: Number) -> int:
    match n:
        case int() as a:
            return a
        case [a, b]:
            return 3 * magnitude(a) + 2 * magnitude(b)
        case _:
            raise ValueError()


def main1() -> int:
    numbers = parse_input()
    res = numbers.pop(0)
    while numbers:
        next_number = numbers.pop(0)
        res = add(res, next_number)
    return magnitude(res)


def main2() -> int:
    max_magnitude = 0
    numbers = parse_input()
    for i, n1 in enumerate(numbers):
        for j, n2 in enumerate(numbers):
            if i == j:
                continue

            res = add(n1, n2)
            max_magnitude = max(max_magnitude, magnitude(res))
    return max_magnitude
