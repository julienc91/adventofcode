from functools import reduce


class CircularList(list[int]):
    def __getitem__(self, index: int | slice) -> int | list[int]:
        if isinstance(index, int):
            return super().__getitem__(index % len(self))
        return [self.__getitem__(i) for i in range(index.start, index.stop)]  # type: ignore

    def __setitem__(self, index: int, value: int) -> None:
        return super().__setitem__(index % len(self), value)


def main1() -> int:
    data_size = 256
    lengths = map(int, input().strip().split(","))
    data: list[int] = CircularList(range(data_size))
    index, skip_size = 0, 0

    for length in lengths:
        data_to_reverse: list[int] = data[index : index + length]  # type: ignore
        for i, c in enumerate(data_to_reverse[::-1]):
            data[index + i] = c

        index += skip_size + length
        skip_size += 1
    return data[0] * data[1]  # type: ignore


def main2() -> str:
    data_size = 256
    lengths = list(map(ord, input().strip())) + [17, 31, 73, 47, 23]
    total_rounds = 64

    data = CircularList(range(data_size))
    index, skip_size = 0, 0

    for _ in range(total_rounds):
        for length in lengths:
            data_to_reverse: list[int] = data[index : index + length]  # type: ignore
            for i, c in enumerate(data_to_reverse[::-1]):
                data[index + i] = c

            index += skip_size + length
            skip_size += 1

    block_size = 16
    dense_hash = ""
    for i in range(0, data_size, block_size):
        block = data[i : i + block_size]
        block_reduction: int = reduce(lambda a, b: a ^ b, block)  # type: ignore
        dense_hash += "{:02x}".format(block_reduction)
    return dense_hash
