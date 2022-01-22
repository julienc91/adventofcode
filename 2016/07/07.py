from typing import Iterator


def parse_addresses() -> Iterator[str]:
    try:
        while line := input().strip():
            yield line
    except EOFError:
        pass


def is_tls(address: str) -> bool:
    bracket_level = 0
    i = 0
    found_pattern = False

    while i < len(address):
        c = address[i]
        if c == "[":
            bracket_level += 1
        elif c == "]":
            bracket_level -= 1
        else:
            block = address[i : i + 4]
            if len(block) < 4:
                break
            if block[0] == block[3] and block[1] == block[2] and block[0] != block[1]:
                if bracket_level > 0:
                    return False
                found_pattern = True
        i += 1
    return found_pattern


def is_ssl(address: str) -> bool:
    bracket_level = 0
    i = 0
    patterns_in_brackets: set[str] = set()
    patterns_outside_brackets: set[str] = set()

    while i < len(address):
        c = address[i]
        if c == "[":
            bracket_level += 1
        elif c == "]":
            bracket_level -= 1
        else:
            block = address[i : i + 3]
            if len(block) < 3:
                break
            if block[0] == block[2] and block[0] != block[1]:
                if bracket_level > 0:
                    patterns_in_brackets.add(block)
                else:
                    patterns_outside_brackets.add(f"{block[1]}{block[0]}{block[1]}")
        i += 1
    return bool(patterns_in_brackets & patterns_outside_brackets)


def main1() -> int:
    return sum(1 for address in parse_addresses() if is_tls(address))


def main2() -> int:
    return sum(1 for address in parse_addresses() if is_ssl(address))
