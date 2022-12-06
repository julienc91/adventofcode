def _main(group_size: int) -> int:
    signal = input().strip()

    counter = group_size - 1
    group = signal[: group_size - 1]
    for char in signal[group_size - 1 :]:
        counter += 1
        if len(set(group + char)) == group_size:
            break
        group = group[1:] + char

    return counter


def main1() -> int:
    return _main(4)


def main2() -> int:
    return _main(14)
