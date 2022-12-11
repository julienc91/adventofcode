def parse_input() -> dict[int, int]:
    layers: dict[int, int] = {}
    try:
        while line := input().strip():
            depth, range_ = map(int, line.split(": "))
            layers[depth] = range_
    except EOFError:
        pass
    return layers


def main1() -> int:
    layers = parse_input()
    caught = []
    max_depth = max(layers.keys())
    for depth in range(max_depth + 1):
        if depth not in layers:
            continue

        range_ = layers[depth]
        if (depth % (2 * (range_ - 1))) == 0:
            caught.append(depth * range_)
    return sum(caught)


def main2() -> int:
    layers = parse_input()
    max_depth = max(layers.keys())
    delay = 0
    while True:
        for depth in range(max_depth + 1):
            if depth not in layers:
                continue

            range_ = layers[depth]
            if ((delay + depth) % (2 * (range_ - 1))) == 0:
                break
        else:
            return delay

        delay += 1
