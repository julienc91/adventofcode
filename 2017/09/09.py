def main1() -> int:
    stream = input().strip()
    in_garbage_block = False
    cancel_char = False
    score = 0
    group_level = 0

    for c in stream:
        if cancel_char:
            cancel_char = False
        elif c == "!":
            cancel_char = True
        elif c == "<" and not in_garbage_block:
            in_garbage_block = True
        elif c == ">":
            assert in_garbage_block
            in_garbage_block = False
        elif in_garbage_block:
            continue
        elif c == "{":
            group_level += 1
            score += group_level
        elif c == "}":
            group_level -= 1
    return score


def main2() -> int:
    stream = input().strip()
    in_garbage_block = False
    cancel_char = False
    count_garbage = 0

    for c in stream:
        if cancel_char:
            cancel_char = False
        elif c == "!":
            cancel_char = True
        elif c == "<" and not in_garbage_block:
            in_garbage_block = True
        elif c == ">":
            assert in_garbage_block
            in_garbage_block = False
        elif in_garbage_block:
            count_garbage += 1
    return count_garbage
