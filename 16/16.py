import math
from dataclasses import dataclass
from enum import Enum
from io import StringIO


class PacketTypes(Enum):
    SUM = 0
    PRODUCT = 1
    MIN = 2
    MAX = 3
    LITTERAL = 4
    GREATER = 5
    LOWER = 6
    EQUAL = 7


@dataclass
class Packet:
    version: int
    type: PacketTypes
    litteral_value: int
    subpackets: list["Packet"]

    @property
    def value(self) -> int:
        if self.type == PacketTypes.SUM:
            return sum(packet.value for packet in self.subpackets)
        elif self.type == PacketTypes.PRODUCT:
            return math.prod(packet.value for packet in self.subpackets)
        elif self.type == PacketTypes.MAX:
            return max(packet.value for packet in self.subpackets)
        elif self.type == PacketTypes.MIN:
            return min(packet.value for packet in self.subpackets)
        elif self.type == PacketTypes.LITTERAL:
            return self.litteral_value
        elif self.type == PacketTypes.GREATER:
            return 1 if self.subpackets[0].value > self.subpackets[1].value else 0
        elif self.type == PacketTypes.LOWER:
            return 1 if self.subpackets[0].value < self.subpackets[1].value else 0
        elif self.type == PacketTypes.EQUAL:
            return 1 if self.subpackets[0].value == self.subpackets[1].value else 0
        raise ValueError(f"Unexpected packet type: {self.type}")


def _read_litteral_value(buffer: StringIO) -> int:
    res = ""
    while group := buffer.read(5):
        res += group[1:]
        if group[0] == "0":
            break
    return int(res, 2)


def init_buffer() -> StringIO:
    hexa_data = input().strip()
    data = "".join(bin(int(c, 16))[2:].zfill(4) for c in hexa_data)
    return StringIO(data)


def parse_packet(buffer: StringIO) -> Packet:
    version = int(buffer.read(3), 2)
    packet_type = PacketTypes(int(buffer.read(3), 2))

    litteral_value = -1
    subpackets: list[Packet] = []

    if packet_type == PacketTypes.LITTERAL:
        litteral_value = _read_litteral_value(buffer)
    else:
        length_type = int(buffer.read(1))
        if length_type == 0:
            subpackets_size = int(buffer.read(15), 2)
            subbuffer = StringIO(buffer.read(subpackets_size))
            subpackets = []
            try:
                while subbuffer:
                    subpackets.append(parse_packet(subbuffer))
            except ValueError:
                pass
        else:
            nb_subpackets = int(buffer.read(11), 2)
            subpackets = [parse_packet(buffer) for _ in range(nb_subpackets)]

    return Packet(
        version=version,
        type=packet_type,
        litteral_value=litteral_value,
        subpackets=subpackets,
    )


def main1() -> int:
    buffer = init_buffer()
    packet = parse_packet(buffer)

    queue = [packet]
    sum_version = 0
    while queue:
        packet = queue.pop()
        sum_version += packet.version
        queue.extend(packet.subpackets)
    return sum_version


def main2() -> int:
    buffer = init_buffer()
    packet = parse_packet(buffer)
    return packet.value


if __name__ == "__main__":
    main1()
