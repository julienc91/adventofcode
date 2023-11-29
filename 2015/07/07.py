from collections.abc import Callable

from utils.parsing import parse_input


def get_value_from_wire_or_raw_signal(
    wire_or_signal: str, circuit: dict[str, int]
) -> int:
    if wire_or_signal.isdigit():
        return int(wire_or_signal)
    return circuit[wire_or_signal]


def update_circuit(instruction: str, circuit: dict[str, int]) -> None:
    if "NOT" in instruction:
        _, v, _, wire = instruction.split()
        value = get_value_from_wire_or_raw_signal(v, circuit)
        circuit[wire] = (2**16) - value - 1

    elif "AND" in instruction or "OR" in instruction or "SHIFT" in instruction:
        v1, operator, v2, _, wire = instruction.split()
        value1 = get_value_from_wire_or_raw_signal(v1, circuit)
        value2 = get_value_from_wire_or_raw_signal(v2, circuit)

        operation: Callable[[int, int], int] = {
            "AND": lambda a, b: a & b,
            "OR": lambda a, b: a | b,
            "LSHIFT": lambda a, b: a << b,
            "RSHIFT": lambda a, b: a >> b,
        }[operator]
        circuit[wire] = operation(value1, value2)

    else:
        v, _, wire = instruction.split()
        value = get_value_from_wire_or_raw_signal(v, circuit)
        circuit[wire] = value


def compute_circuit(instructions: list[str]) -> dict[str, int]:
    circuit: dict[str, int] = {}
    while instructions:
        instruction = instructions.pop(0)
        try:
            update_circuit(instruction, circuit)
        except KeyError:
            instructions.append(instruction)
    return circuit


def main1() -> int:
    instructions = list(parse_input())
    circuit = compute_circuit(instructions)
    return circuit["a"]


def main2() -> int:
    instructions = list(parse_input())
    circuit = compute_circuit(instructions[:])

    instructions = [f"{circuit['a']} -> b"] + [
        instruction for instruction in instructions if not instruction.endswith(" -> b")
    ]
    circuit = compute_circuit(instructions)
    return circuit["a"]
