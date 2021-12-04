def main1() -> int:
    x, y = 0, 0
    try:
        while command := input():
            move, value = command.split()
            nb = int(value)
            if move == "forward":
                x += nb
            elif move == "down":
                y += nb
            elif move == "up":
                y -= nb
            else:
                raise ValueError(f"Unknown command {move}")
    except EOFError:
        return x * y
    raise RuntimeError


def main2() -> int:
    x, y, aim = 0, 0, 0
    try:
        while command := input():
            move, value = command.split()
            nb = int(value)
            if move == "forward":
                x += nb
                y += aim * nb
            elif move == "down":
                aim += nb
            elif move == "up":
                aim -= nb
            else:
                raise ValueError(f"Unknown command {move}")
    except EOFError:
        return x * y
    raise RuntimeError


if __name__ == "__main__":
    result = main2()
    print(result)
