import itertools
import random
from dataclasses import dataclass

from utils.parsing import parse_input

funcs = {
    "OR": lambda u, v: u | v,
    "AND": lambda u, v: u & v,
    "XOR": lambda u, v: u ^ v,
}


@dataclass(frozen=True)
class Gate:
    x: str
    operator: str
    y: str

    def __hash__(self):
        return hash(tuple(sorted([self.x, self.operator, self.y])))


def parse_variables() -> dict[str, bool]:
    variables = {}
    for line in parse_input():
        if not line:
            break
        name, value = line.split(": ")
        value = value == "1"
        variables[name] = value
    return variables


def parse_gates() -> dict[Gate, str]:
    gates = {}
    for line in parse_input():
        a, operator, b, c = line.replace(" -> ", " ").split()
        gates[Gate(a, operator, b)] = c
    return gates


def get_input_size(gates: dict[Gate, str]) -> int:
    return int(max(gates.values())[1:])


def execute(variables: dict[str, bool], gates: dict[Gate, str]) -> str:
    queue = [(k, v) for k, v in gates.items()]
    already_seen = None
    while queue:
        gate, out = queue.pop(0)
        try:
            val_x = variables[gate.x]
            val_y = variables[gate.y]
        except KeyError:
            assert gate != already_seen, gate  # Infinite loop detector
            queue.append((gate, out))
            if already_seen is None:
                already_seen = gate
            continue

        assert out not in variables
        already_seen = None

        variables[out] = funcs[gate.operator](val_x, val_y)

    input_size = get_input_size(gates)
    return "".join(str(int(variables[f"z{i:02d}"])) for i in range(input_size, -1, -1))


def main1() -> int:
    variables = parse_variables()
    gates = parse_gates()
    bin_val = execute(variables, gates)
    return int(bin_val, 2)


def execute_from_values(x: int, y: int, gates: dict[Gate, str]) -> int:
    input_size = get_input_size(gates)
    bin_x = bin(x)[2:].zfill(input_size)
    bin_y = bin(y)[2:].zfill(input_size)
    variables = {f"x{i:02d}": b == "1" for i, b in enumerate(bin_x[::-1])} | {
        f"y{i:02d}": b == "1" for i, b in enumerate(bin_y[::-1])
    }
    return int(execute(variables, gates), 2)


def identify_wrong_bits(gates: dict[Gate, str]) -> set[int]:
    input_size = get_input_size(gates)
    wrong_bits = set()
    for i in range(input_size):
        res = execute_from_values(1 << i, 0, gates)
        if res != (1 << i):
            wrong_bits.add(i)
    return wrong_bits


def find_possible_swaps_for_bit(
    bit: int, gates: dict[Gate, str]
) -> list[tuple[str, str]]:
    queue = [f"x{bit:02d}"]
    downward_dependencies = set()
    while queue:
        var_name = queue.pop()
        for gate, out in gates.items():
            if gate.x == var_name or gate.y == var_name:
                downward_dependencies.add(out)
                queue.append(out)

    queue = [f"z{bit:02d}", f"z{bit + 1:02d}"]
    upward_dependencies = set(queue)
    while queue:
        var_name = queue.pop()
        for gate, out in gates.items():
            if out == var_name:
                upward_dependencies.add(gate.x)
                upward_dependencies.add(gate.y)
                queue += [gate.x, gate.y]

    nodes = downward_dependencies & upward_dependencies
    possible_swaps = []
    for swap in itertools.combinations(list(nodes), 2):
        new_gates = _apply_swap(swap, gates)
        try:
            if bit not in identify_wrong_bits(new_gates):
                possible_swaps.append(swap)
        except AssertionError:
            continue
    return possible_swaps


def _apply_swap(swap: tuple[str, str], gates: dict[Gate, str]) -> dict[Gate, str]:
    gates = gates.copy()
    a, b = swap
    for gate, out in gates.items():
        if out == a:
            gates[gate] = b
        elif out == b:
            gates[gate] = a
    return gates


def check_gates(gates: dict[Gate, str]) -> bool:
    input_size = get_input_size(gates)
    for _ in range(10):
        x = random.randint(0, 1 << input_size)
        y = random.randint(0, 1 << input_size)
        try:
            res = execute_from_values(x, y, gates)
        except AssertionError:
            return False
        if res != x + y:
            return False
    return True


def find_correct_swap(
    gates: dict[Gate, str], possible_swaps: dict[int, list[tuple[str, str]]]
) -> list[tuple[str, str]]:
    for combination in itertools.product(*[swaps for swaps in possible_swaps.values()]):
        new_gates = gates.copy()
        for swap in combination:
            new_gates = _apply_swap(swap, new_gates)
        if check_gates(new_gates):
            return list(combination)
    raise RuntimeError()


def main2() -> str:
    _ = parse_variables()
    gates = parse_gates()
    wrong_bits = identify_wrong_bits(gates)
    possible_swaps = {
        bit: find_possible_swaps_for_bit(bit, gates) for bit in wrong_bits
    }
    swaps = find_correct_swap(gates, possible_swaps)
    res = []
    for a, b in swaps:
        res += [a, b]
    return ",".join(sorted(res))
