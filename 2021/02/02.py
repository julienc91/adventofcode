from utils.parsing import parse_input


def main1() -> int:
    x, y = 0, 0
    for command in parse_input():
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
    return x * y


def main2() -> int:
    x, y, aim = 0, 0, 0
    for command in parse_input():
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
    return x * y
