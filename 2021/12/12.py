from collections import defaultdict


def parse_paths() -> dict[str, list[str]]:
    paths = defaultdict(list)
    try:
        while line := input().strip():
            a, b = line.split("-")
            paths[a].append(b)
            paths[b].append(a)
    except EOFError:
        pass
    return paths


def count_paths(
    stack: list[str], paths: dict[str, list[str]], revisit_one_small_cave: bool
) -> int:
    current_cave = stack[-1]
    possible_next_caves = paths[current_cave]
    result = 0

    for next_cave in possible_next_caves:
        assert next_cave != current_cave
        if next_cave == "end":
            result += 1
        elif next_cave == "start":
            continue
        elif next_cave.islower() and next_cave in stack:
            if revisit_one_small_cave is False:
                continue
            result += count_paths(
                [*stack, next_cave], paths, revisit_one_small_cave=False
            )
        else:
            result += count_paths(
                [*stack, next_cave],
                paths,
                revisit_one_small_cave=revisit_one_small_cave,
            )
    return result


def main1() -> int:
    paths = parse_paths()
    stack = ["start"]
    return count_paths(stack, paths, revisit_one_small_cave=False)


def main2() -> int:
    paths = parse_paths()
    stack = ["start"]
    return count_paths(stack, paths, revisit_one_small_cave=True)
