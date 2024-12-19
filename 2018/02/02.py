import itertools
from collections import Counter
from collections.abc import Iterator

from utils.parsing import parse_input


def parse_boxes() -> Iterator[str]:
    yield from parse_input()


def main1() -> int:
    count_threes = 0
    count_twos = 0
    for box in parse_boxes():
        counter = Counter(box)
        if 3 in counter.values():
            count_threes += 1
        if 2 in counter.values():
            count_twos += 1
    return count_threes * count_twos


def main2() -> str:
    boxes = list(parse_boxes())
    for box1, box2 in itertools.combinations(boxes, 2):
        res = ""
        error = False
        for c1, c2 in zip(box1, box2, strict=True):
            if c1 == c2:
                res += c1
            elif error:
                break
            else:
                error = True
        else:
            return res
    raise RuntimeError()
