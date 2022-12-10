from collections import defaultdict
from collections.abc import Callable


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
    try:
        while line := input().strip():
            operation, condition = line.split(" if ")
            if evaluate_condition(registers, condition):
                evaluate_operation(registers, operation)
    except EOFError:
        pass
    return max(registers.values())


def main2() -> int:
    registers: dict[str, int] = defaultdict(int)
    response = 0
    try:
        while line := input().strip():
            operation, condition = line.split(" if ")
            if evaluate_condition(registers, condition):
                value = evaluate_operation(registers, operation)
                response = max(response, value)
    except EOFError:
        pass
    return response
