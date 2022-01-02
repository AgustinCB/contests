import sys
from typing import List


class Packet(object):
    def __init__(self, version: int, package_type: int):
        self.version = version
        self.type = package_type

    def sum_versions(self):
        return self.version


class LiteralPacket(Packet):
    def __init__(self, version: int, package_type: int, literal: int):
        super().__init__(version, package_type)
        self.literal = literal

    def eval(self) -> int:
        return self.literal

    def __str__(self):
        return "[Literal Packet, version={}, type={}, literal={}]".format(self.version, self.type, self.literal)

    def __repr__(self):
        return self.__str__()


class OperatorPacket(Packet):
    def __init__(self, version: int, package_type: int, length_type_id: int, length_value: int, subpackets: List[Packet]):
        super().__init__(version, package_type)
        self.length_type_id = length_type_id
        self.length_value = length_value
        self.subpackets = subpackets

    def sum_versions(self):
        return sum([s.sum_versions() for s in self.subpackets]) + self.version

    def __str__(self):
        return "[Operator Packet, version={}, type={}, subpackets={}]".format(self.version, self.type, self.subpackets)

    def __repr__(self):
        return self.__str__()


def bits_to_int(bits: List[int]) -> int:
    return int(''.join([str(c) for c in bits]), 2)


def parse_literal_packet(bits: List[int], packet_version: int, packet_type: int) -> (LiteralPacket, List[int]):
    literal_bits = []
    bit_group = 0
    more_bit_groups = True
    while more_bit_groups:
        more_bit_groups = bool(bits[bit_group * 5])
        literal_bits.extend(bits[bit_group * 5 + 1:(bit_group + 1) * 5])
        bit_group += 1
    literal = bits_to_int(literal_bits)
    return LiteralPacket(packet_version, packet_type, literal), bits[bit_group * 5:]


def parse_operator_packet_by_subpackets_bit_length(
        bits: List[int], packet_version: int, packet_type: int
) -> (OperatorPacket, List[int]):
    subpackets_bit_size = bits_to_int(bits[:15])
    pending_bits = bits[15:15+subpackets_bit_size]
    subpackets = []
    while len(pending_bits) > 0:
        subpacket, pending_bits = parse_packet(pending_bits)
        subpackets.append(subpacket)
    return OperatorPacket(packet_version, packet_type, 1, subpackets_bit_size, subpackets), bits[15+subpackets_bit_size:]


def parse_operator_packet_by_subpackets_length(
        bits: List[int], packet_version: int, packet_type: int
) -> (OperatorPacket, List[int]):
    subpackets_length = bits_to_int(bits[:11])
    pending_bits = bits[11:]
    subpackets = []
    for _ in range(subpackets_length):
        subpacket, pending_bits = parse_packet(pending_bits)
        subpackets.append(subpacket)
    return OperatorPacket(packet_version, packet_type, 0, subpackets_length, subpackets), pending_bits


def parse_operator_packet(bits: List[int], packet_version: int, packet_type: int) -> (OperatorPacket, List[int]):
    length_type_id = bits[0]
    if length_type_id == 0:
        return parse_operator_packet_by_subpackets_bit_length(bits[1:], packet_version, packet_type)
    else:
        return parse_operator_packet_by_subpackets_length(bits[1:], packet_version, packet_type)


def parse_packet(bits: List[int]) -> (Packet, List[int]):
    packet_version = bits_to_int(bits[0:3])
    packet_type = bits_to_int(bits[3:6])
    if packet_type == 4:
        return parse_literal_packet(bits[6:], packet_version, packet_type)
    else:
        return parse_operator_packet(bits[6:], packet_version, packet_type)


def hex_to_four_digits_binary(hex: str) -> str:
    result = bin(int(hex, 16)).replace('0b', '')
    if len(result) < 4:
        return "0" * (4 - len(result)) + result
    return result


def solve():
    bits = [int(c) for c in ''.join([hex_to_four_digits_binary(c) for c in sys.stdin.readline().strip()])]
    packet = parse_packet(bits)[0]
    print(packet)
    return packet.sum_versions()


if __name__ == '__main__':
    print(solve())
