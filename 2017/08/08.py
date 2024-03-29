from collections import defaultdict
from collections.abc import Callable

from utils.parsing import parse_input


def evaluate_condition(registers: dict[str, int], condition: str) -> bool:
    register, operator, value = condition.split()
    func: Callable[[int, int], bool] = {
        ">": lambda a, b: a > b,
        ">=": lambda a, b: a >= b,
        "<": lambda a, b: a < b,
        "<=": lambda a, b: a <= b,
        "==": lambda a, b: a == b,
        "!=": lambda a, b: a != b,
    }[operator]
    return func(registers[register], int(value))


def evaluate_operation(registers: dict[str, int], operation: str) -> int:
    register, operator, value = operation.split()
    func: Callable[[int, int], int] = {
        "inc": lambda a, b: a + b,
        "dec": lambda a, b: a - b,
    }[operator]
    registers[register] = func(registers[register], int(value))
    return registers[register]


def main1() -> int:
    registers: dict[str, int] = defaultdict(int)
    for line in parse_input():
        operation, condition = line.split(" if ")
        if evaluate_condition(registers, condition):
            evaluate_operation(registers, operation)
    return max(registers.values())


def main2() -> int:
    registers: dict[str, int] = defaultdict(int)
    response = 0
    for line in parse_input():
        operation, condition = line.split(" if ")
        if evaluate_condition(registers, condition):
            value = evaluate_operation(registers, operation)
            response = max(response, value)
    return response
