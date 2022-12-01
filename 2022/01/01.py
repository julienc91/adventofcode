def _main() -> list[int]:
    elves = [0]
    try:
        while True:
            line = input().strip()
            if not line:
                elves.append(0)
            else:
                elves[-1] += int(line)
    except EOFError:
        pass
    return sorted(elves)


def main1() -> int:
    return _main()[-1]


def main2() -> int:
    return sum(_main()[-3:])
