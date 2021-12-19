def do_step(data: str) -> str:
    previous_c = data[0]
    count = 1
    res = ""
    for c in data[1:]:
        if c == previous_c:
            count += 1
        else:
            res += f"{count}{previous_c}"
            count = 1
        previous_c = c

    res += f"{count}{previous_c}"
    return res


def _main(nb_steps: int) -> int:
    data = input().strip()
    for _ in range(nb_steps):
        data = do_step(data)
    return len(data)


def main1() -> int:
    return _main(40)


def main2() -> int:
    return _main(50)
