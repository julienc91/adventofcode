def _main(size: int) -> int:
    data = input().strip()
    while len(data) < size:
        data += "0" + "".join("1" if c == "0" else "0" for c in data[::-1])
    data = data[:size]

    checksum = ""
    while len(checksum) % 2 == 0:
        checksum = "".join(
            "1" if c0 == c1 else "0" for c0, c1 in zip(data[::2], data[1::2])
        )
        data = checksum

    return int(checksum)


def main1() -> int:
    return _main(size=272)


def main2() -> int:
    return _main(size=35651584)
