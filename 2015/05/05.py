from collections.abc import Callable, Iterator


def parse_input() -> Iterator[str]:
    try:
        while line := input().strip():
            yield line
    except EOFError:
        pass


def is_nice_v1(string: str) -> bool:
    previous_letter = ""
    count_voyels = 0
    has_duplicated_letter = False

    for c in string:
        if c == previous_letter:
            has_duplicated_letter = True
        if previous_letter + c in ("ab", "cd", "pq", "xy"):
            return False
        if c in "aeiou":
            count_voyels += 1
        previous_letter = c
    return has_duplicated_letter and count_voyels >= 3


def is_nice_v2(string: str) -> bool:
    has_repeated_pair = False
    has_repeater_letter = False
    for i in range(len(string)):
        try:
            if not has_repeated_pair:
                pair = string[i : i + 2]
                if pair in string[i + 2 :]:
                    has_repeated_pair = True

            if not has_repeater_letter:
                if string[i] == string[i + 2]:
                    has_repeater_letter = True
        except IndexError:
            return False

        if has_repeated_pair and has_repeater_letter:
            return True
    return False


def main_(is_nice: Callable[[str], bool]) -> int:
    res = 0
    for string in parse_input():
        if is_nice(string):
            res += 1
    return res


def main1() -> int:
    return main_(is_nice_v1)


def main2() -> int:
    return main_(is_nice_v2)
