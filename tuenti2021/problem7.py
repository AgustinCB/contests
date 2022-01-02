from collections import defaultdict
from queue import Queue
import socket
from typing import Dict

HOST = 'codechallenge-daemons.0x14.net'
PORT = 4321

CACHED_DUNGEON = {'0x0': ['1x0'], '1x0': ['1x1', '2x0', '0x0'], '2x0': ['3x0', '1x0'], '3x0': ['4x0', '2x0'], '4x0': ['5x0', '3x0'], '5x0': ['6x0', '4x0'], '6x0': ['6x1', '5x0'], '6x1': ['6x2', '6x0'], '6x2': ['6x1', '7x2', '5x2'], '5x2': ['6x2'], '7x2': ['6x2'], '1x1': ['1x2', '1x0'], '1x2': ['1x1', '2x2'], '2x2': ['2x3', '3x2', '1x2'], '3x2': ['2x2'], '2x3': ['2x4', '2x2'], '2x4': ['2x3', '3x4'], '3x4': ['3x5', '4x4', '2x4'], '4x4': ['5x4', '3x4'], '5x4': ['6x4', '4x4'], '6x4': ['6x5', '5x4'], '6x5': ['6x6', '6x4', '7x5'], '7x5': ['8x5', '6x5'], '8x5': ['9x5', '7x5'], '9x5': ['10x5', '8x5'], '10x5': ['11x5', '9x5'], '11x5': ['12x5', '10x5'], '12x5': ['13x5', '11x5'], '13x5': ['13x6', '13x4', '14x5', '12x5'], '14x5': ['15x5', '13x5'], '15x5': ['14x5'], '13x4': ['13x5', '13x3'], '13x3': ['13x4', '13x2', '12x3'], '12x3': ['13x3', '11x3'], '11x3': ['12x3', '10x3'], '10x3': ['11x3', '9x3'], '9x3': ['9x2', '10x3', '8x3'], '8x3': ['9x3'], '9x2': ['9x3', '9x1'], '9x1': ['9x2', '10x1'], '10x1': ['10x0', '11x1', '9x1'], '11x1': ['12x1', '10x1'], '12x1': ['13x1', '11x1'], '13x1': ['13x2', '14x1', '12x1'], '14x1': ['15x1', '13x1'], '15x1': ['15x0', '14x1'], '15x0': ['15x1', '16x0'], '16x0': ['17x0', '15x0'], '17x0': ['18x0', '16x0'], '18x0': ['19x0', '17x0'], '19x0': ['18x0'], '13x2': ['13x3', '13x1', '13x3', '13x1'], '10x0': ['10x1'], '13x6': ['13x5'], '6x6': ['6x7', '6x5'], '6x7': ['6x6', '7x7'], '7x7': ['7x8', '8x7', '6x7'], '8x7': ['9x7', '7x7'], '9x7': ['8x7'], '7x8': ['7x9', '7x7'], '7x9': ['7x10', '7x8'], '7x10': ['7x11', '7x9', '8x10'], '8x10': ['9x10', '7x10'], '9x10': ['10x10', '8x10'], '10x10': ['11x10', '9x10'], '11x10': ['11x11', '11x9', '12x10', '10x10'], '12x10': ['13x10', '11x10'], '13x10': ['13x11', '13x9', '12x10'], '13x9': ['13x10', '13x8'], '13x8': ['13x9', '14x8'], '14x8': ['15x8', '13x8'], '15x8': ['16x8', '14x8'], '16x8': ['16x7', '15x8'], '16x7': ['16x8', '16x6'], '16x6': ['16x7', '17x6'], '17x6': ['17x5', '16x6'], '17x5': ['17x6', '17x4'], '17x4': ['17x5', '18x4'], '18x4': ['19x4', '17x4'], '19x4': ['18x4'], '13x11': ['13x10', '14x11'], '14x11': ['15x11', '13x11'], '15x11': ['16x11', '14x11'], '16x11': ['16x12', '17x11', '15x11'], '17x11': ['18x11', '16x11'], '18x11': ['18x10', '19x11', '17x11'], '19x11': ['19x12', '18x11'], '19x12': ['19x11'], '18x10': ['18x11', '18x9'], '18x9': ['18x10', '18x8'], '18x8': ['18x9', '19x8'], '19x8': ['18x8'], '16x12': ['16x13', '16x11'], '16x13': ['16x14', '16x12'], '16x14': ['16x13', '17x14', '15x14'], '15x14': ['16x14', '14x14'], '14x14': ['15x14', '13x14'], '13x14': ['14x14'], '17x14': ['18x14', '16x14'], '18x14': ['19x14', '17x14'], '19x14': ['19x15', '18x14'], '19x15': ['19x16', '19x14'], '19x16': ['19x17', '19x15'], '19x17': ['19x16', '18x17'], '18x17': ['18x18', '19x17'], '18x18': ['18x19', '18x17'], '18x19': ['18x18', '17x19'], '17x19': ['18x19', '16x19'], '16x19': ['16x18', '17x19'], '16x18': ['16x19', '15x18'], '15x18': ['16x18', '14x18'], '14x18': ['15x18', '13x18'], '13x18': ['13x17', '14x18'], '13x17': ['13x18', '13x16'], '13x16': ['13x17', '12x16'], '12x16': ['13x16', '11x16'], '11x16': ['11x15', '12x16', '10x16'], '10x16': ['11x16', '9x16'], '9x16': ['10x16', '8x16'], '8x16': ['9x16', '7x16'], '7x16': ['7x17', '7x15', '8x16'], '7x15': ['7x16', '7x14'], '7x14': ['7x15', '7x13', '6x14'], '6x14': ['7x14', '5x14'], '5x14': ['6x14', '4x14'], '4x14': ['4x15', '5x14', '3x14'], '3x14': ['4x14', '2x14'], '2x14': ['2x13', '3x14', '1x14'], '1x14': ['2x14', '0x14'], '0x14': ['1x14'], '2x13': ['2x14', '2x12'], '2x12': ['2x13', '2x11'], '2x11': ['2x12', '2x10'], '2x10': ['2x11', '2x9'], '2x9': ['2x10', '2x8'], '2x8': ['2x9', '2x7'], '2x7': ['2x8', '3x7', '1x7'], '1x7': ['2x7', '0x7'], '0x7': ['1x7'], '3x7': ['3x6', '4x7', '2x7'], '4x7': ['3x7'], '3x6': ['3x7', '3x5'], '3x5': ['3x6', '3x4', '3x6', '3x4'], '4x15': ['4x16', '4x14'], '4x16': ['4x17', '4x15'], '4x17': ['4x18', '4x16', '3x17'], '3x17': ['4x17', '2x17'], '2x17': ['3x17', '1x17'], '1x17': ['2x17', '0x17'], '0x17': ['1x17'], '4x18': ['4x19', '4x17'], '4x19': ['4x18'], '7x13': ['7x14', '7x12'], '7x12': ['7x13', '7x11'], '7x11': ['7x12', '7x10', '7x12', '7x10'], '7x17': ['7x18', '7x16'], '7x18': ['7x19', '7x17'], '7x19': ['7x18'], '11x15': ['11x16', '11x14'], '11x14': ['11x15', '11x13'], '11x13': ['11x14', '11x12'], '11x12': ['11x13', '11x11'], '11x11': ['11x12', '11x10', '11x12', '11x10'], '11x9': ['11x10']}
CACHED_EXIT_POSITION = (19, 17)


def send_message(s: socket.socket, message: str) -> str:
    print(message)
    s.sendall(bytes(message, "utf-8"))
    result = s.recv(4096).decode("utf-8").strip()
    print(result)
    return result


def go_to(s: socket.socket, x: int, y: int):
    send_message(s, "go to {},{}\n".format(x, y))


def is_exit(s: socket.socket, x: int, y: int) -> bool:
    result = send_message(s, "is exit?\n")
    return result != "No. Sorry, traveller..."


def get_neighbors(s: socket.socket, x: int, y: int) -> [[int]]:
    result = send_message(s, "look\n")
    directions = result.replace("Well, well, well, my friend. You could do these movements: ", "").split(" ")
    neighbors = []
    for direction in directions:
        if direction == 'west':
            neighbors.append([x + 1, y])
        if direction == 'east':
            neighbors.append([x - 1, y])
        if direction == 'north':
            neighbors.append([x, y + 1])
        if direction == 'south':
            neighbors.append([x, y - 1])
    return neighbors


def build_dungeon_map():
    if CACHED_DUNGEON is not None and CACHED_EXIT_POSITION is not None:
        return CACHED_DUNGEON, CACHED_EXIT_POSITION
    dungeon = defaultdict(list)
    exit_position = None
    queue = [(0, 0)]
    visited = set()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(s.recv(4096).decode("utf-8").strip())
        while len(queue) > 0:
            x, y = queue.pop()
            visited.add("{}x{}".format(x, y))
            go_to(s, x, y)
            if is_exit(s, x, y):
                exit_position = (x, y)
            neighbors = get_neighbors(s, x, y)
            for nx, ny in neighbors:
                position = "{}x{}".format(nx, ny)
                dungeon["{}x{}".format(x, y)].append(position)
                if position not in visited:
                    queue.append([nx, ny])
    return dungeon, exit_position


def find_shortest_path(dungeon: Dict[str, list], start_position: [int], exit_position: [int]) -> [[int]]:
    queue = Queue()
    queue.put_nowait([start_position])
    while queue.qsize() > 0:
        path = queue.get_nowait()
        node = path[-1]
        if node == exit_position:
            return [[int(c) for c in p.split('x')] for p in path]
        for adjacent in dungeon[node]:
            if adjacent not in path:
                new_path = list(path)
                new_path.append(adjacent)
                queue.put_nowait(new_path)


def solve():
    (dungeon, exit_position) = build_dungeon_map()
    shortest_path = find_shortest_path(dungeon, "0x0", "{}x{}".format(exit_position[0], exit_position[1]))
    print(", ".join(["({}, {})".format(x, y) for x, y in shortest_path]))


if __name__ == '__main__':
    solve()

