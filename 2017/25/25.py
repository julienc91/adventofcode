from utils.regex import findone

State = tuple[int, int, str]


def parse_input() -> tuple[str, int, dict[str, dict[int, State]]]:
    start = findone(r"Begin in state (\w)", input())
    steps = int(findone(r"Perform a diagnostic checksum after (\d+) steps.", input()))
    input()
    states = {}
    while True:
        try:
            state = findone(r"In state (\w):", input())
            states[state] = {}
            for _ in range(2):
                value = int(findone(r"If the current value is (\d):", input()))
                write = int(findone(r"- Write the value (\d)", input()))
                move = findone(r"- Move one slot to the (left|right)", input())
                direction = 1 if move == "right" else -1
                next_state = findone(r"- Continue with state (\w)", input())
                states[state][value] = (write, direction, next_state)
            input()
        except EOFError:
            break
    return start, steps, states


def main1() -> int:
    start, steps, states = parse_input()

    state = start
    tape = {}
    cursor = 0
    while steps > 0:
        value = tape.get(cursor, 0)
        write, direction, next_state = states[state][value]
        if write == 1:
            tape[cursor] = write
        else:
            tape.pop(cursor, None)
        cursor += direction
        state = next_state
        steps -= 1
    return len(tape)


def main2() -> int:
    return -1
