from collections.abc import Callable

from utils.parsing import parse_input


def _main(checker: Callable[[str], bool]) -> int:
    counter = 0
    for line in parse_input():
        if checker(line):
            counter += 1
    return counter


def main1() -> int:
    def is_valid(line: str) -> bool:
        words = line.split()
        return len(words) == len(set(words))

    return _main(is_valid)


def main2() -> int:
    def is_valid(line: str) -> bool:
        words = line.split()
        return (
            len(words)
            == len(set(words))
            == len(set("".join(sorted(word)) for word in words))
        )

    return _main(is_valid)
