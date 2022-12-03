import itertools
import string
import sys

priorities = {char: index for index, char in enumerate(string.ascii_letters, start=1)}


def main1() -> int:
    priority = 0
    try:
        while line := input().strip():
            left = set(line[: len(line) // 2])
            right = set(line[len(line) // 2 :])
            duplicate = (left & right).pop()
            priority += priorities[duplicate]
    except EOFError:
        pass
    return priority


def main2() -> int:
    priority = 0
    group_size = 3
    iterator = map(str.strip, sys.stdin)
    while True:
        group = itertools.islice(iterator, group_size)
        lines = [set(line) for line in group]
        if not lines:
            break
        duplicate = set.intersection(*lines).pop()
        priority += priorities[duplicate]
    return priority
