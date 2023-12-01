from utils.parsing import parse_input


def get_combinations(containers: list[int], total: int) -> set[tuple[int, ...]]:
    containers = sorted(containers, reverse=True)
    named_containers = [(i, c) for i, c in enumerate(containers, start=1)]
    combinations: set[tuple[int, ...]] = set()

    def _inner(
        stack: list[int], subtotal: int, remaining: list[tuple[int, int]]
    ) -> None:
        if subtotal == total:
            combinations.add(tuple(stack))
            return
        if subtotal > total or not remaining:
            return

        for i in range(len(remaining)):
            _inner(
                [*stack, remaining[i][0]],
                subtotal + remaining[i][1],
                remaining[i + 1 :],
            )

    _inner([], 0, named_containers)
    return combinations


def main1() -> int:
    total = 150
    containers = list(parse_input(int))
    combinations = get_combinations(containers, total)
    return len(combinations)


def main2() -> int:
    total = 150
    containers = list(parse_input(int))
    combinations = get_combinations(containers, total)

    min_size = len(containers)
    count = 0
    for combination in combinations:
        if len(combination) < min_size:
            min_size = len(combination)
            count = 1
        elif len(combination) == min_size:
            count += 1
    return count
