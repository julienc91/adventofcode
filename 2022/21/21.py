from typing import Callable

OPERATORS: dict[str, Callable[[int, int], int]] = {
    "+": lambda a, b: a + b,
    "/": lambda a, b: a // b,
    "*": lambda a, b: a * b,
    "-": lambda a, b: a - b,
}
REVERSE_LEFT: dict[str, Callable[[int, int], int]] = {
    "+": lambda right, target: target - right,
    "/": lambda right, target: target * right,
    "*": lambda right, target: target // right,
    "-": lambda right, target: target + right,
}
REVERSE_RIGHT: dict[str, Callable[[int, int], int]] = {
    "+": lambda left, target: target - left,
    "/": lambda left, target: left // target,
    "*": lambda left, target: target // left,
    "-": lambda left, target: left - target,
}


def parse_input() -> dict[str, int | tuple[str, str, str]]:
    res: dict[str, int | tuple[str, str, str]] = {}
    try:
        while line := input().strip():
            name, operation = line.split(": ")
            if operation.isdigit():
                res[name] = int(operation)
            else:
                left, operator, right = operation.split(" ")
                res[name] = (left, right, operator)
    except EOFError:
        pass
    return res


def compute(name: str, data: dict[str, int | tuple[str, str, str]]) -> int:
    operation = data[name]
    if isinstance(operation, int):
        return operation

    left, right, operator = operation
    left_value = compute(left, data)
    right_value = compute(right, data)
    operator_func = OPERATORS[operator]
    result = operator_func(left_value, right_value)
    data[name] = result
    return result


def solve(
    name: str, data: dict[str, int | tuple[str, str, str]], target_value: int
) -> int:
    if name == "humn":
        return target_value

    value = data[name]
    if isinstance(value, int):
        return value

    left, right, operator = value
    try:
        left_value = compute(left, data)
        sub_branch = right
        operator_func = REVERSE_RIGHT[operator]
        target_value = operator_func(left_value, target_value)
    except KeyError:
        right_value = compute(right, data)
        sub_branch = left
        operator_func = REVERSE_LEFT[operator]
        target_value = operator_func(right_value, target_value)
    return solve(sub_branch, data, target_value)


def main1() -> int:
    data = parse_input()
    return compute("root", data)


def main2() -> int:
    data = parse_input()
    del data["humn"]

    value = data["root"]
    assert not isinstance(value, int)
    left, right, operator = value
    data["root"] = (left, right, "-")
    return solve("root", data, 0)
