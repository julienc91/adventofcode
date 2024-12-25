def parse_locks_and_keys() -> tuple[list[list[int]], list[list[int]]]:
    locks, keys = [], []
    w, h = 5, 6
    while True:
        line = input()
        assert len(line) == w, len(line)
        is_lock = line.startswith("#")

        pattern = [0 for _ in range(w)]
        for i in range(h):
            line = input()
            assert len(line) == w
            for j, c in enumerate(line):
                if c == ("#" if is_lock else "."):
                    pattern[j] += 1

        if is_lock:
            locks.append(pattern)
        else:
            pattern = [h - 1 - v for v in pattern]
            keys.append(pattern)

        try:
            input()
        except EOFError:
            break
    return locks, keys


def main1() -> int:
    locks, keys = parse_locks_and_keys()
    count = 0
    for key in keys:
        for lock in locks:
            if all(a + b < 6 for a, b in zip(key, lock, strict=True)):
                count += 1
    return count


def main2() -> int:
    return -1
