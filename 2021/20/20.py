def parse_algorithm() -> list[bool]:
    line = input().strip()
    input()
    return [c == "#" for c in line]


def parse_image() -> list[list[bool]]:
    res = []
    try:
        while line := input().strip():
            res.append([c == "#" for c in line])
    except EOFError:
        pass
    return res


def get_pixel(image: list[list[bool]], x: int, y: int, step: int) -> bool:
    if y < 0 or y >= len(image) or x < 0 or x >= len(image[y]):
        return bool((step) % 2)
    return image[y][x]


def get_algorithm_index(image: list[list[bool]], x: int, y: int, step: int) -> int:
    neighbour_coordinates = [
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    ]
    neighbour_values = map(
        int, [get_pixel(image, a, b, step) for a, b in neighbour_coordinates]
    )
    return int("".join(map(str, neighbour_values)), 2)


def scale_image(image: list[list[bool]], step: int) -> list[list[bool]]:
    fill = (step % 2) == 1
    res = [
        [fill for _ in range(len(image[0]))],
        *image,
        [fill for _ in range(len(image[0]))],
    ]
    for y in range(len(res)):
        res[y] = [fill, *res[y], fill]
    return res


def process_image(
    image: list[list[bool]], algorithm: list[bool], step: int
) -> list[list[bool]]:
    res: list[list[bool]] = []
    image = scale_image(image, step)
    for y in range(len(image)):
        res.append([])
        for x in range(len(image[y])):
            index = get_algorithm_index(image, x, y, step)
            res[y].append(algorithm[index])
    return res


def display_image(image: list[list[bool]]) -> None:
    for y in range(len(image)):
        line = []
        for x in range(len(image[y])):
            line.append("#" if image[y][x] else ".")
        print("".join(line))
    print()


def _main(nb_steps: int) -> int:
    algorithm = parse_algorithm()
    image = parse_image()

    for step in range(nb_steps):
        image = process_image(image, algorithm, step)

    return sum(1 for row in image for cell in row if cell)


def main1() -> int:
    return _main(2)


def main2() -> int:
    return _main(50)
