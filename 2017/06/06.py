from collections.abc import Iterator


def iterate_states() -> Iterator[tuple[int, ...]]:
    banks = [int(i) for i in input().strip().split()]
    while True:
        yield tuple(banks)
        max_value = max(banks)
        index = banks.index(max_value)
        banks[index] = 0
        for i in range(max_value):
            banks[(index + 1 + i) % len(banks)] += 1


def main1() -> int:
    visited: set[tuple[int, ...]] = set()
    for state in iterate_states():
        if state in visited:
            break
        visited.add(state)
    return len(visited)


def main2() -> int:
    visited: dict[tuple[int, ...], int] = {}
    for i, state in enumerate(iterate_states()):
        if state in visited:
            return i - visited[state]
        visited[state] = i
    raise RuntimeError()
