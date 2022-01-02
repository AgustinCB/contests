import sys


def solve():
    prev_depth = None
    counter = 0
    depths = []
    for line in sys.stdin:
        depth = int(line)
        depths.append(depth)

    for depth_index in range(2, len(depths)):
        window = [depths[depth_index], depths[depth_index - 1], depths[depth_index - 2]]
        depth = sum(window)
        if prev_depth is not None and depth > prev_depth:
            counter += 1
        prev_depth = depth
    return counter


if __name__ == '__main__':
    print(solve())
