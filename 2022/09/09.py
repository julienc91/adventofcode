def is_neighbour(head: tuple[int, int], tail: tuple[int, int]) -> bool:
    x1, y1 = head
    x2, y2 = tail
    return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1


def move_tail(head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
    if is_neighbour(head, tail):
        return tail

    xh, yh = head
    xt, yt = tail
    if xt != xh:
        xt += 1 if xh > xt else -1
    if yt != yh:
        yt += 1 if yh > yt else -1
    return xt, yt


def _main(rope_length: int) -> int:
    rope = [(0, 0) for _ in range(rope_length)]
    visited = {rope[-1]}
    try:
        while line := input().strip():
            xh, yh = rope[0]
            direction, count = line.split()
            for _ in range(int(count)):
                if direction in {"U", "D"}:
                    yh += 1 if direction == "U" else -1
                else:
                    xh += 1 if direction == "R" else -1
                rope[0] = (xh, yh)

                for i in range(rope_length - 1):
                    rope[i + 1] = move_tail(rope[i], rope[i + 1])
                visited.add(rope[-1])
    except EOFError:
        pass
    return len(visited)


def main1() -> int:
    return _main(2)


def main2() -> int:
    return _main(10)
