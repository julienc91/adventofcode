from collections import Counter
from typing import Iterator


def parse_rooms() -> Iterator[tuple[str, str, int]]:
    try:
        while line := input().strip():
            checksum = line[-6:-1]
            name, remaining = line.rsplit("-", 1)
            sector_id = int(remaining.split("[")[0])
            yield name, checksum, sector_id
    except EOFError:
        pass


def is_real_room(name: str, checksum: str) -> bool:
    name = name.replace("-", "")
    counter = [(-count, char) for char, count in Counter(name).items()]
    counter.sort()
    expected_checksum = "".join(c for _, c in counter[:5])
    return expected_checksum == checksum


def decode(name: str, sector_id: int) -> str:
    res = ""
    for c in name:
        if c == "-":
            res += " "
        else:
            res += chr(((ord(c) - ord("a") + sector_id) % 26) + ord("a"))
    return res


def main1() -> int:
    res = 0
    for name, checksum, sector_id in parse_rooms():
        if is_real_room(name, checksum):
            res += sector_id
    return res


def main2() -> int:
    for name, checksum, sector_id in parse_rooms():
        if not is_real_room(name, checksum):
            continue
        name = decode(name, sector_id)
        if name == "northpole object storage":
            return sector_id
    raise RuntimeError()
