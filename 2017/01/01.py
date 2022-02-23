def _main(s: str, n: int) -> int:
    return sum(int(a) if a == b else 0 for a, b in zip(s, s[n:] + s[:n]))


def main1() -> int:
    s = input().strip()
    return _main(s, 1)


def main2() -> int:
    s = input().strip()
    return _main(s, len(s) // 2)
