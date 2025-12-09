import itertools

from utils.parsing import parse_input


def parse_tiles() -> list[tuple[int, int]]:
    res = []
    for line in parse_input():
        x, y = map(int, line.split(","))
        res.append((x, y))
    return res


def get_area(a: tuple[int, int], b: tuple[int, int]) -> int:
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def get_tile_pairs_with_area(
    tiles: list[tuple[int, int]],
) -> list[tuple[tuple[int, int], tuple[int, int], int]]:
    return [
        (val[0], val[1], get_area(val[0], val[1]))
        for val in itertools.combinations(tiles, 2)
    ]


def main1() -> int:
    tiles = parse_tiles()
    _, _, res = max(get_tile_pairs_with_area(tiles), key=lambda val: val[2])
    return res


def get_edges(tiles: list[tuple[int, int]]) -> set[tuple[int, int]]:
    edges = set()
    for i in range(len(tiles)):
        x1, y1 = tiles[i - 1]
        x2, y2 = tiles[i]
        if x1 == x2:
            edges |= {(x1, y) for y in range(min(y1, y2), max(y1, y2) + 1)}
        elif y1 == y2:
            edges |= {(x, y1) for x in range(min(x1, x2), max(x1, x2) + 1)}
        else:
            raise ValueError("Edge is not straight")
    return edges


def main2():
    tiles = parse_tiles()
    edges = get_edges(tiles)

    tile_pairs = sorted(
        get_tile_pairs_with_area(tiles), key=lambda val: val[2], reverse=True
    )
    for (x1, y1), (x2, y2), area in tile_pairs:
        x_min, x_max = sorted((x1, x2))
        y_min, y_max = sorted((y1, y2))
        for x, y in edges:
            if x_min < x < x_max and y_min < y < y_max:
                break
        else:
            return area

    raise RuntimeError("No solution found")
