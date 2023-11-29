from utils.parsing import parse_input


def parse_discs() -> list[tuple[int, int]]:
    res: list[tuple[int, int]] = []
    for line in parse_input():
        line = line.rstrip(".")
        _, _, _, nb_pos, _, _, _, _, _, _, _, start_pos = line.split()
        res.append((int(nb_pos), int(start_pos)))
    return res


def _main(discs: list[tuple[int, int]]) -> int:
    t = 0
    while True:
        for i, (nb_pos, start_pos) in enumerate(discs, start=1):
            pos = (i + start_pos + t) % nb_pos
            if pos != 0:
                t += nb_pos - pos
                break
        else:
            return t


def main1() -> int:
    discs = parse_discs()
    return _main(discs)


def main2() -> int:
    discs = parse_discs()
    discs.append((11, 0))
    return _main(discs)
