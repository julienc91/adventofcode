def parse_instructions() -> list[str]:
    res: list[str] = []
    try:
        while line := input().strip():
            res.append(line)
    except EOFError:
        pass
    return res


def swap_position(key: list[str], a: int, b: int) -> list[str]:
    key[a], key[b] = key[b], key[a]
    return key


def swap_letter(key: list[str], a: str, b: str) -> list[str]:
    ai, bi = key.index(a), key.index(b)
    key[ai], key[bi] = key[bi], key[ai]
    return key


def reverse_rotate_based(key: list[str], a: str) -> list[str]:
    tmp = key
    while rotate_based(tmp, a) != key:
        tmp = rotate_left(tmp, 1)
    return tmp


def rotate_based(key: list[str], a: str) -> list[str]:
    i = key.index(a)
    i += 2 if i >= 4 else 1
    return rotate_right(key, i)


def rotate_right(key: list[str], i: int) -> list[str]:
    i = i % len(key)
    return key[-i:] + key[:-i]


def rotate_left(key: list[str], i: int) -> list[str]:
    i = i % len(key)
    return key[i:] + key[:i]


def reverse_positions(key: list[str], a: int, b: int) -> list[str]:
    key = key[:a] + key[a : b + 1][::-1] + key[b + 1 :]
    return key


def move_position(key: list[str], a: int, b: int) -> list[str]:
    char = key.pop(a)
    key.insert(b, char)
    return key


def apply_instruction(key: list[str], instruction: str) -> list[str]:
    words = instruction.split()
    if instruction.startswith("swap position"):
        key = swap_position(key, int(words[2]), int(words[5]))
    elif instruction.startswith("swap letter"):
        key = swap_letter(key, words[2], words[5])
    elif instruction.startswith("rotate based"):
        key = rotate_based(key, words[6])
    elif instruction.startswith("rotate left"):
        key = rotate_left(key, int(words[2]))
    elif instruction.startswith("rotate right"):
        key = rotate_right(key, int(words[2]))
    elif instruction.startswith("reverse positions"):
        key = reverse_positions(key, int(words[2]), int(words[4]))
    elif instruction.startswith("move position"):
        key = move_position(key, int(words[2]), int(words[5]))
    else:
        raise RuntimeError(f"Unexpected instruction: {instruction}")
    return key


def apply_reverse_instruction(key: list[str], instruction: str) -> list[str]:
    words = instruction.split()
    if instruction.startswith("swap position"):
        key = swap_position(key, int(words[2]), int(words[5]))
    elif instruction.startswith("swap letter"):
        key = swap_letter(key, words[2], words[5])
    elif instruction.startswith("rotate based"):
        key = reverse_rotate_based(key, words[6])
    elif instruction.startswith("rotate left"):
        key = rotate_right(key, int(words[2]))
    elif instruction.startswith("rotate right"):
        key = rotate_left(key, int(words[2]))
    elif instruction.startswith("reverse positions"):
        key = reverse_positions(key, int(words[2]), int(words[4]))
    elif instruction.startswith("move position"):
        key = move_position(key, int(words[5]), int(words[2]))
    else:
        raise RuntimeError(f"Unexpected instruction: {instruction}")
    return key


def main1() -> str:
    key = list("abcdefgh")
    instructions = parse_instructions()
    for instruction in instructions:
        key = apply_instruction(key, instruction)
    return "".join(key)


def main2() -> str:
    key = list("fbgdceah")
    instructions = parse_instructions()[::-1]
    for instruction in instructions:
        key = apply_reverse_instruction(key, instruction)
    return "".join(key)
