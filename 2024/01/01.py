from collections import Counter

from utils.parsing import parse_input


def parse_lists() -> tuple[list[int], list[int]]:
    l1, l2 = [], []
    for line in parse_input():
        n1, n2 = list(map(int, line.split()))
        l1.append(n1)
        l2.append(n2)
    return l1, l2


def main1() -> int:
    l1, l2 = parse_lists()
    l1.sort()
    l2.sort()
    return sum(abs(a - b) for a, b in zip(l1, l2, strict=True))


def main2() -> int:
    l1, l2 = parse_lists()
    counter = Counter(l2)
    return sum(i * counter[i] for i in l1)
