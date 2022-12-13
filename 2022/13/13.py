import math
from ast import literal_eval
from functools import cmp_to_key

Packet = int | list[int | list["Packet"]]


def parse_input() -> list[tuple[Packet, Packet]]:
    pairs: list[tuple[Packet, Packet]] = []
    try:
        while True:
            packet1 = literal_eval(input().strip())
            packet2 = literal_eval(input().strip())
            pairs.append((packet1, packet2))

            _ = input()
    except EOFError:
        pass
    return pairs


def compare_packets(packet1: Packet, packet2: Packet) -> int:
    match (packet1, packet2):
        case (int(), int()) as packets:
            if packets[0] == packets[1]:
                return 0
            return -1 if packets[0] < packets[1] else 1
        case (int(), _):
            return compare_packets([packet1], packet2)
        case (_, int()):
            return compare_packets(packet1, [packet2])
        case ([], []):
            return 0
        case ([], _):
            return -1
        case (_, []):
            return 1
        case ([a, *rest1], [b, *rest2]):
            compare = compare_packets(a, b)
            if compare == 0:
                return compare_packets(rest1, rest2)
            return compare
        case _ as e:
            raise ValueError(e)


def main1() -> int:
    packets = parse_input()
    result = 0
    for i, pair in enumerate(packets, start=1):
        if compare_packets(*pair) <= 0:
            result += i
    return result


def main2() -> int:
    dividers: list[Packet] = [[[2]], [[6]]]
    packets: list[Packet] = [*dividers]
    for pair in parse_input():
        packets += [pair[0], pair[1]]
    packets.sort(key=cmp_to_key(compare_packets))

    indexes: list[int] = []
    for i, packet in enumerate(packets, start=1):
        if packet in dividers:
            indexes.append(i)
    assert len(indexes) == len(dividers)
    return math.prod(indexes)
