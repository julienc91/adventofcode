from collections import defaultdict


def _main(nb_days: int) -> int:
    data: dict[int, int] = defaultdict(int)
    for i in input().split(","):
        data[int(i)] += 1

    for day in range(nb_days):
        new_data: dict[int, int] = defaultdict(int)
        for nb_days, nb_fish in data.items():
            if nb_days == 0:
                new_data[8] += nb_fish
                new_data[6] += nb_fish
            else:
                new_data[nb_days - 1] += nb_fish
        data = new_data
    return sum(data.values())


def main1() -> int:
    return _main(nb_days=80)


def main2() -> int:
    return _main(nb_days=256)
