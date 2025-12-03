from utils.parsing import parse_input


def get_max_joltage(line: list[int], count: int) -> int:
    def find_next_digit(rest: list[int], length: int) -> tuple[int, list[int]]:
        if len(rest) < length:
            raise ValueError
        elif len(rest) == length:
            return rest[0], rest[1:]

        candidate, candidate_idx = 0, 0
        for k in range(len(rest) - length + 1):
            if rest[k] > candidate:
                candidate = rest[k]
                candidate_idx = k

        return candidate, rest[candidate_idx + 1 :]

    res = []
    for i in range(count):
        digit, line = find_next_digit(line, count - i)
        res.append(digit)

    return int("".join(map(str, res)))


def _main(count: int) -> int:
    return sum(get_max_joltage(list(map(int, line)), count) for line in parse_input())


def main1() -> int:
    return _main(2)


def main2() -> int:
    return _main(12)
