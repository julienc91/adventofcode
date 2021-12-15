from collections import Counter


def parse_formula() -> str:
    line = input().strip()
    input()
    return line


def parse_transformations() -> dict[tuple[str, str], str]:
    res = {}
    try:
        while line := input().strip():
            a, b = line.split(" -> ")
            res[(a[0], a[1])] = b
    except EOFError:
        pass
    return res


def do_step(
    counter: Counter[tuple[str, str]], transformations: dict[tuple[str, str], str]
) -> Counter[tuple[str, str]]:
    updated_counter: Counter[tuple[str, str]] = Counter()
    for pair, count in counter.items():
        insertion = transformations.get(pair, "")
        if not insertion:
            updated_counter[pair] = count
        else:
            pair1, pair2 = (pair[0], insertion), (insertion, pair[1])
            updated_counter[pair1] += count
            updated_counter[pair2] += count
    return updated_counter


def _main(nb_steps: int) -> int:
    formula = parse_formula()
    transformations = parse_transformations()

    pair_counter: Counter[tuple[str, str]] = Counter()
    for i in range(1, len(formula)):
        pair_counter[(formula[i - 1], formula[i])] += 1

    for i in range(nb_steps):
        pair_counter = do_step(pair_counter, transformations)

    char_counter: Counter[str] = Counter()
    for pair, count in pair_counter.items():
        a, b = pair
        char_counter[a] += count
        char_counter[b] += count

    sorted_entries = char_counter.most_common()
    most_common_count, least_common_count = (
        sorted_entries[0][1] / 2,
        sorted_entries[-1][1] / 2,
    )
    return int(most_common_count - least_common_count)


def main1() -> int:
    return _main(10)


def main2() -> int:
    return _main(40)
