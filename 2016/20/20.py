def parse_blocklists() -> list[tuple[int, int]]:
    res: list[tuple[int, int]] = []
    try:
        while line := input():
            a, b = line.split("-")
            res.append((int(a), int(b)))
    except EOFError:
        pass
    return res


def minify_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    a, b = ranges[0]
    minified_ranges = []
    for x, y in ranges[1:]:
        if x <= b + 1:
            b = max(b, y)
        else:
            minified_ranges.append((a, b))
            a, b = x, y
    minified_ranges.append((a, b))
    return minified_ranges


def _main() -> list[tuple[int, int]]:
    blocklists = sorted(parse_blocklists())
    return minify_ranges(blocklists)


def main1() -> int:
    blocklists = _main()
    if blocklists[0][0] > 0:
        return 0
    return blocklists[0][1] + 1


def main2() -> int:
    blocklists = _main()
    total_blocked = sum(b - a + 1 for a, b in blocklists)
    return 2**32 - total_blocked
