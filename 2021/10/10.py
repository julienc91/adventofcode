from collections.abc import Iterator

pairs = {")": "(", "]": "[", "}": "{", ">": "<"}


def parse_input() -> Iterator[str]:
    try:
        while line := input().strip():
            yield line
    except EOFError:
        pass


def build_stack(line: str) -> tuple[str | None, list[str]]:
    stack = []
    for c in line:
        if c in "([{<":
            stack.append(c)
            continue

        try:
            last = stack.pop()
        except IndexError:
            return c, stack

        if pairs[c] != last:
            return c, stack

    return None, stack


def main1() -> int:
    points = {")": 3, "]": 57, "}": 1197, ">": 25137}
    result = 0
    for line in parse_input():
        invalid_char, _ = build_stack(line)
        if invalid_char is not None:
            result += points[invalid_char]
    return result


def main2() -> int:
    points = {"(": 1, "[": 2, "{": 3, "<": 4}
    scores = []
    for line in parse_input():
        score = 0
        invalid_char, stack = build_stack(line)
        if invalid_char is not None:
            continue
        while stack:
            c = stack.pop()
            score = score * 5 + points[c]
        scores.append(score)

    scores.sort()
    result = scores[len(scores) // 2]
    return result
