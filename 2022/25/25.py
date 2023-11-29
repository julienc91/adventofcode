from utils.parsing import parse_input


def snafu_to_dec(number: str) -> int:
    res = 0
    for i, c in enumerate(number[::-1]):
        res += {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}[c] * (5**i)
    return res


def dec_to_snafu(number: int) -> str:
    res = ""
    while number > 0:
        digit = "012=-"[number % 5]
        number = (2 + number) // 5
        res = digit + res
    return res


def main1() -> str:
    count = 0
    for line in parse_input():
        count += snafu_to_dec(line)
    return dec_to_snafu(count)


def main2() -> int:
    return -1
