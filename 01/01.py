def main(window_size: int) -> int:
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


if __name__ == "__main__":
    result = main(window_size=3)
    print(result)
