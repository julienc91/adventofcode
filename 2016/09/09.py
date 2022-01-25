def count_sequence_length(data: str, recursive: bool) -> int:
    try:
        open_index = data.index("(")
        close_index = data.index(")")
        multiplier = data[open_index + 1 : close_index]
        a, b = map(int, multiplier.split("x"))

        if recursive:
            return b * count_sequence_length(
                data[close_index + 1 : close_index + 1 + a], True
            ) + count_sequence_length(data[close_index + 1 + a :], True)
        else:
            return b * a + count_sequence_length(data[close_index + 1 + a :], False)
    except ValueError:
        return len(data)


def main1() -> int:
    data = input().strip()
    return count_sequence_length(data, False)


def main2() -> int:
    data = input().strip()
    return count_sequence_length(data, True)
