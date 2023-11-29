from utils.parsing import parse_input


def _main(window_size: int) -> int:
    result = 0
    previous_window = [int(input()) for _ in range(window_size)]
    for current_value in parse_input():
        current_window = [*previous_window[1:], int(current_value)]
        if sum(current_window) > sum(previous_window):
            result += 1
        previous_window = current_window
    return result


def main1() -> int:
    return _main(1)


def main2() -> int:
    return _main(3)
