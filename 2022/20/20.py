from collections import deque


class Mixer:
    def __init__(self, data: list[int]) -> None:
        self.data = data

    def mix(self, n: int = 1) -> list[int]:
        indexes = deque(i for i in range(len(self.data)))
        data = deque(self.data)
        for _ in range(n):
            for i in range(len(self.data)):
                index = indexes.index(i)

                data.rotate(-index)
                indexes.rotate(-index)
                number = data.popleft()
                indexes.popleft()

                data.rotate(-number)
                indexes.rotate(-number)
                data.appendleft(number)
                indexes.appendleft(i)

        self.data = list(data)
        return self.data


def parse_input() -> list[int]:
    res: list[int] = []
    try:
        while line := input().strip():
            res.append(int(line))
    except EOFError:
        pass
    return res


def find_grove_coordinates(data: list[int]) -> int:
    index_0 = data.index(0)
    return sum(
        [
            data[(index_0 + 1000) % len(data)],
            data[(index_0 + 2000) % len(data)],
            data[(index_0 + 3000) % len(data)],
        ]
    )


def main1() -> int:
    data = parse_input()
    mixer = Mixer(data)

    mix_result = mixer.mix()
    return find_grove_coordinates(mix_result)


def main2() -> int:
    data = parse_input()
    decryption_key = 811589153
    data = list(map(lambda n: n * decryption_key, data))

    mixer = Mixer(data)
    mix_result = mixer.mix(10)
    return find_grove_coordinates(mix_result)
