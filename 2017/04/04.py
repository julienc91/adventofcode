from collections.abc import Callable


def _main(checker: Callable[[str], bool]) -> int:
    counter = 0
    try:
        while line := input().strip():
            if checker(line):
                counter += 1
    except EOFError:
        pass
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
