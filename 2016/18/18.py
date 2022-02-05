def parse_input() -> tuple[bool, ...]:
    return tuple(c == "^" for c in input().strip())


def get_next_row(current_row: tuple[bool, ...]) -> tuple[tuple[bool, ...], int]:
    next_row = []
    row_size = len(current_row)
    count_safe = 0
    for i in range(row_size):
        left = current_row[i - 1] if i > 0 else False
        right = current_row[i + 1] if i < row_size - 1 else False
        val = left is not right
        if not val:
            count_safe += 1
        next_row.append(val)
    return tuple(next_row), count_safe


def _main(total_rows: int) -> int:
    current_row = parse_input()
    current_row_index = 1
    total_safe_tiles = current_row.count(False)

    while current_row_index < total_rows:
        current_row, safe_tiles = get_next_row(current_row)
        current_row_index += 1
        total_safe_tiles += safe_tiles
    return total_safe_tiles


def main1() -> int:
    return _main(40)


def main2() -> int:
    return _main(400000)
