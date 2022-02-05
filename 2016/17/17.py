import hashlib
from collections import deque
from typing import Iterator


def get_available_neighbours(
    x: int, y: int, path: str, key: str
) -> list[tuple[int, int, str]]:
    neighbours = [(x, y - 1, "U"), (x, y + 1, "D"), (x - 1, y, "L"), (x + 1, y, "R")]
    hash_ = hashlib.md5((key + path).encode()).hexdigest()[:4]
    res: list[tuple[int, int, str]] = []
    for (x, y, dir_), c in zip(neighbours, hash_):
        if c in "bcdef" and 0 <= x < 4 and 0 <= y < 4:
            res.append((x, y, path + dir_))
    return res


def _main() -> Iterator[str]:
    x, y = 0, 0
    target = (3, 3)
    key = input().strip()

    stack = deque([(x, y, "")])
    while stack:
        x, y, path = stack.popleft()
        if (x, y) == target:
            yield path
            continue

        for neighbour in get_available_neighbours(x, y, path, key):
            stack.append(neighbour)


def main1() -> str:
    return next(_main())


def main2() -> int:
    *_, longest_path = _main()
    return len(longest_path)
