def parse_input() -> list[tuple[int, int]]:
    res: list[tuple[int, int]] = []
    try:
        while line := input().strip().rstrip("."):
            _, _, _, nb_pos, _, _, _, _, _, _, _, start_pos = line.split()
            res.append((int(nb_pos), int(start_pos)))
    except EOFError:
        pass
    return res


def _main(disqs: list[tuple[int, int]]) -> int:
    t = 0
    while True:
        for i, (nb_pos, start_pos) in enumerate(disqs, start=1):
            pos = (i + start_pos + t) % nb_pos
            if pos != 0:
                t += nb_pos - pos
                break
        else:
            return t


def main1() -> int:
    disqs = parse_input()
    return _main(disqs)


def main2() -> int:
    disqs = parse_input()
    disqs.append((11, 0))
    return _main(disqs)
