from __future__ import annotations

import sys
from typing import Optional, Tuple, Set, Dict


class Node(object):
    def __init__(self, data: int, next_node: Optional[Node]):
        self.data = data
        self.next_node = next_node

    def __str__(self) -> str:
        result = [str(self.data)]
        next_node = self.next_node
        while next_node.data != self.data:
            result.append(str(next_node.data))
            next_node = next_node.next_node
        return ' '.join(result)

    def __repr__(self) -> str:
        return self.__str__()


def build_linked_list(ids: str) -> Node:
    head = Node(int(ids[0]), None)
    current = head
    for current_id in ids[1:]:
        new_node = Node(int(current_id), None)
        current.next_node = new_node
        current = new_node
    current.next_node = head
    return head


def get_next_circular_node(current: Node) -> Node:
    return current.next_node


def get_next_three_nodes(current: Node) -> Tuple[Node, Node, Node]:
    first = current.next_node
    second = first.next_node
    third = second.next_node
    return first, second, third


def get_lower_id(node_id: int, limit: int) -> int:
    destination_id = node_id - 1
    if destination_id == 0:
        destination_id = limit
    return destination_id


def find_destination_cup(starting: Node, picked: Set[int], limit: int, cache: Optional[Dict[int, Node]]) -> Node:
    destination_id = get_lower_id(starting.data, limit)
    while destination_id in picked:
        destination_id = get_lower_id(destination_id, limit)
    if cache is not None:
        return cache[destination_id]
    current = starting
    while current.data != destination_id:
        current = current.next_node
    return current


def place_next_to(prev: Node, node: Node, next_to: Node):
    next_to_next = next_to.next_node
    prev.next_node, node.next_node = node.next_node, next_to_next
    next_to.next_node = node


def play_round(current: Node, limit: int, cache: Optional[Dict[int, Node]]) -> Node:
    first, second, third = get_next_three_nodes(current)
    destination = find_destination_cup(current, {first.data, second.data, third.data}, limit, cache)
    place_next_to(current, first, destination)
    place_next_to(current, second, first)
    place_next_to(current, third, second)
    return current.next_node


def pad(head: Node, limit: int) -> Dict[int, Node]:
    cache = {head.data: head}
    current = head.next_node
    prev = None
    while current.data != head.data:
        cache[current.data] = current
        prev = current
        current = current.next_node
    current = prev
    for i in range(9 + 1, limit + 1):
        current.next_node = Node(i, None)
        cache[current.data] = current
        current = current.next_node
    cache[current.data] = current
    current.next_node = head
    return cache


def play_game(head: Node, iterations: int = 100, limit: int = 9) -> Node:
    current = head
    cache = None
    if limit > 9:
        cache = pad(head, limit)
    for i in range(iterations):
        if limit < 30:
            print(i, current.data, "\t--\t", head)
        elif i % 1000 == 0:
            print(i, current.data)
        current = play_round(current, limit, cache)
    return head


def solve():
    head = build_linked_list(sys.stdin.readline().strip())
    if sys.argv[1] == 'part1':
        before_one, after_one = str(play_game(head)).split('1')
        return "{}{}".format(after_one, before_one).replace(' ', '')
    if sys.argv[1] == 'part2':
        result = play_game(head, 10_000_000, 1_000_000)
        current = result
        while current.data != 1:
            current = current.next_node
        return current.next_node.data * current.next_node.next_node.data


if __name__ == '__main__':
    print(solve())
