def _main(window_size: int) -> int:
    result = 0
    previous_window = [int(input()) for _ in range(window_size)]
    try:
        while current_value := input():
            current_window = [*previous_window[1:], int(current_value)]
            if sum(current_window) > sum(previous_window):
                result += 1
            previous_window = current_window
    except EOFError:
        return result
    raise RuntimeError


def main1() -> int:
    return _main(1)


def main2() -> int:
    return _main(3)
