import typing
from functools import cache, reduce


# Copied from 2017-10
class CircularList(list[int]):
    @typing.no_type_check
    def __getitem__(self, index: int | slice) -> int | list[int]:
        if isinstance(index, int):
            return super().__getitem__(index % len(self))
        return [self.__getitem__(i) for i in range(index.start, index.stop)]

    @typing.no_type_check
    def __setitem__(self, index: int, value: int) -> None:
        return super().__setitem__(index % len(self), value)


def dense_hash(data: list[int]) -> str:
    data_size = 256
    block_size = 16
    result = ""
    for i in range(0, data_size, block_size):
        block_reduction = reduce(lambda a, b: a ^ b, data[i : i + block_size])
        result += "{:02x}".format(block_reduction)
    return result


def hash_knot(input_: str) -> str:
    data_size = 256
    total_rounds = 64
    lengths = list(map(ord, input_)) + [17, 31, 73, 47, 23]

    index, skip_size = 0, 0
    data = CircularList(range(data_size))

    for _ in range(total_rounds):
        for length in lengths:
            data_to_reverse = data[index : index + length][::-1]
            for i, c in enumerate(data_to_reverse):
                data[index + i] = c

            index += skip_size + length
            skip_size += 1

    return dense_hash(data)


@cache
def get_grid(key: str) -> list[str]:
    grid_height = 128
    result: list[str] = []
    for i in range(grid_height):
        hash_input = f"{key}-{i}"
        hash_output = hash_knot(hash_input)
        result.append("".join("{:04b}".format(int(c, 16)) for c in hash_output))
    return result


def visit(
    grid: list[str], start: tuple[int, int], visited: set[tuple[int, int]]
) -> None:
    visited.add(start)
    queue = [start]
    while queue:
        x, y = queue.pop(0)
        for x2, y2 in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if not 0 <= y2 < len(grid) or not 0 <= x2 < len(grid[y2]):
                continue
            if grid[y2][x2] == "0":
                continue
            if (x2, y2) in visited:
                continue
            visited.add((x2, y2))
            queue.append((x2, y2))


def main1() -> int:
    key = input().strip()
    grid = get_grid(key)
    return sum(row.count("1") for row in grid)


def main2() -> int:
    key = input().strip()
    grid = get_grid(key)
    visited: set[tuple[int, int]] = set()
    count_regions = 0

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "0":
                continue
            if (x, y) in visited:
                continue

            visit(grid, (x, y), visited)
            count_regions += 1
    return count_regions
