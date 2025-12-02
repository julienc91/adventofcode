from collections.abc import Iterator


def parse_ranges() -> Iterator[tuple[int, int]]:
    line = input().split(",")
    for r in line:
        a, b = map(int, r.split("-"))
        assert a <= b
        yield a, b


def find_simple_invalid_ids(a: int, b: int) -> list[int]:
    if len(str(a)) < len(str(b)):
        return find_simple_invalid_ids(
            a, int("9" * len(str(a)))
        ) + find_simple_invalid_ids(int("1" + "0" * len(str(a))), b)

    if len(str(a)) % 2 == 1:
        return []

    res = []
    prefix_length = min(len(str(a)) // 2, 1)
    idx = int(str(a)[:prefix_length])
    while True:
        candidate = int(str(idx) + str(idx))
        if candidate > b:
            break
        elif candidate >= a:
            res.append(candidate)
        idx += 1
    return res


def main1() -> int:
    return sum(sum(find_simple_invalid_ids(a, b)) for a, b in parse_ranges())


def find_complex_invalid_ids(a: int, b: int) -> set[int]:
    res = set()
    patterns = set()
    idx = a
    while idx <= b:
        for prefix_length in range(1, len(str(a)) + 1):
            pattern = str(idx)[:prefix_length]
            if pattern in patterns:
                continue

            patterns.add(pattern)
            repeat = 2
            while True:
                candidate = int(str(pattern) * repeat)
                if candidate > b:
                    break
                elif candidate >= a:
                    res.add(candidate)
                repeat += 1

            if repeat == 2:
                break

        idx += 1
    return res


def main2() -> int:
    return sum(sum(find_complex_invalid_ids(a, b)) for a, b in parse_ranges())
