import math


def main1() -> int:
    # https://en.wikipedia.org/wiki/Josephus_problem#k=2
    nb_elves = int(input())
    return int(2 * (nb_elves - (2 ** int(math.log2(nb_elves)))) + 1)


def process(n: int) -> int:
    elves = list(range(1, n + 1))
    while len(elves) > 1:
        i = len(elves) // 2
        elves.pop(i)
        elves = elves[1:] + [elves[0]]
    return elves[0]


def main2() -> int:
    # Empirical, based on first results of `process`
    nb_elves = int(input())
    log = int(math.log(nb_elves, 3))
    if 3**log == nb_elves:
        return nb_elves

    latest_power = int(3**log)
    if nb_elves <= 2 * latest_power:
        return nb_elves - latest_power
    else:
        return 2 * nb_elves - 3 * latest_power
