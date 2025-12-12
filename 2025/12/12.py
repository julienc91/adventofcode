from utils.parsing import parse_input

Shape = list[list[bool]]
Problem = tuple[tuple[int, int], list[int]]


def parse_data() -> tuple[list[Shape], list[Problem]]:
    shapes = []
    current_shape = []
    problems = []
    for line in parse_input():
        if not line:
            if current_shape:
                shapes.append(current_shape)
                current_shape = []
        elif line.endswith(":"):
            current_shape = []
        elif line.startswith(("#", ".")):
            current_shape.append([c == "#" for c in line])
        else:
            left, *right = line.split(" ")
            x, y = map(int, left.removesuffix(":").split("x"))
            problems.append(((x, y), list(map(int, right))))
    return shapes, problems


def get_shapes_sizes(shapes: list[Shape]) -> list[int]:
    res = []
    for shape in shapes:
        size = 0
        for row in shape:
            size += row.count(True)
        res.append(size)
    return res


def solve_with_big_assumption(shapes: list[Shape], problem: Problem) -> bool:
    (x, y), shape_counts = problem
    shape_sizes = get_shapes_sizes(shapes)
    grid_size = x * y
    sum_of_sizes = 0
    for i, shape_count in enumerate(shape_counts):
        sum_of_sizes += shape_sizes[i] * shape_count
    return sum_of_sizes <= grid_size


def main1() -> int:
    shapes, problems = parse_data()
    res = 0
    for problem in problems:
        if solve_with_big_assumption(shapes, problem):
            res += 1
    return res


def main2() -> int:
    return -1
