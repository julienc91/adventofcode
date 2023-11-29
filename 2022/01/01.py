from utils.parsing import parse_input


def _main() -> list[int]:
    elves = [0]
    for line in parse_input():
        if not line:
            elves.append(0)
        else:
            elves[-1] += int(line)
    return sorted(elves)


def main1() -> int:
    return _main()[-1]


def main2() -> int:
    return sum(_main()[-3:])
