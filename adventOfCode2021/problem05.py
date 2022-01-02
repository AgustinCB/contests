import sys


def solve():
    bits_info = [[0, 0] for _ in range(13)]
    for line in sys.stdin:
        for (index, bit) in enumerate(line):
            if bit == "\n":
                continue
            bit = int(bit)
            bits_info[index][bit] += 1

    gamma = 0
    epsilon = 0
    power = 0
    bits_info.reverse()
    for bits in bits_info:
        if bits[0] == bits[1] == 0: continue
        if bits[0] > bits[1]:
            epsilon += 2 ** power
        else:
            gamma += 2 ** power
        power += 1
    return epsilon * gamma


if __name__ == '__main__':
    print(solve())
