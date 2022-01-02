from __future__ import annotations

import math
import sys
from typing import Set, Optional


class SnailfishNumber(object):
    def __init__(
            self,
            left: Optional[SnailfishNumber],
            right: Optional[SnailfishNumber],
            data: Optional[int],
            level: int,
    ):
        self.left = left
        self.right = right
        self.data = data
        self.level = level
        self.root = None

    def set_root(self, root: SnailfishNumber):
        if root != self:
            self.root = root
        else:
            self.root = None
        if self.left is not None:
            self.left.set_root(root)
        if self.right is not None:
            self.right.set_root(root)

    def sum(self, other: SnailfishNumber) -> SnailfishNumber:
        self.increase_level()
        other.increase_level()
        new_root = SnailfishNumber(self, other, None, 1)
        new_root.set_root(new_root)
        return new_root

    def increase_level(self):
        self.level += 1
        if self.left is not None:
            self.left.increase_level()
        if self.right is not None:
            self.right.increase_level()

    def find_id_for(self, node: SnailfishNumber) -> int:
        stack = [self]
        current_id = 0
        while len(stack) > 0:
            current_node = stack.pop()
            if current_node == node:
                return current_id
            if current_node.data is not None:
                current_id += 1
            else:
                stack.append(current_node.right)
                stack.append(current_node.left)
        raise RuntimeError("Node {} not found in {}".format(node, node.root))

    def find_node_from_id(self, search_id: int) -> Optional[SnailfishNumber]:
        stack = [self]
        current_id = 0
        while stack:
            current_node = stack.pop()
            if current_node.data is not None and current_id == search_id:
                return current_node
            elif current_node.data is not None:
                current_id += 1
            else:
                stack.append(current_node.right)
                stack.append(current_node.left)
        return None

    def reduce(self):
        while self.__explode() or self.__split():
            continue

    def __explode(self) -> bool:
        if self.data is None and self.level == 5:
            left_id = self.root.find_id_for(self.left)
            right_id = self.root.find_id_for(self.right)
            if left_id != 0:
                to_update_on_left = self.root.find_node_from_id(left_id - 1)
                if to_update_on_left and to_update_on_left.data is not None:
                    to_update_on_left.data += self.left.data
            to_update_on_right = self.root.find_node_from_id(right_id + 1)
            if to_update_on_right and to_update_on_right.data is not None:
                to_update_on_right.data += self.right.data
            self.left = None
            self.right = None
            self.data = 0
            return True
        if self.left is not None:
            if self.left.__explode():
                return True
        if self.right is not None:
            if self.right.__explode():
                return True
        return False

    def __split(self) -> bool:
        if self.data is not None and self.data > 9:
            self.left = SnailfishNumber(None, None, math.floor(self.data / 2), self.level + 1)
            self.right = SnailfishNumber(None, None, math.ceil(self.data / 2), self.level + 1)
            self.data = None
            self.set_root(self.root)
            return True
        if self.left is not None:
            if self.left.__split():
                return True
        if self.right is not None:
            if self.right.__split():
                return True
        return False

    def magnitude(self) -> int:
        if self.data is not None:
            return self.data
        return self.left.magnitude() * 3 + self.right.magnitude() * 2

    @staticmethod
    def parse(array_form: [], level: int) -> SnailfishNumber:
        if isinstance(array_form[0], int):
            left = SnailfishNumber(None, None, array_form[0], level + 1)
        else:
            left = SnailfishNumber.parse(array_form[0], level + 1)
        if isinstance(array_form[1], int):
            right = SnailfishNumber(None, None, array_form[1], level + 1)
        else:
            right = SnailfishNumber.parse(array_form[1], level + 1)
        result = SnailfishNumber(left, right, None, level)
        result.set_root(result)
        return result

    def __str__(self):
        """
        return "[Node\n{}left={},\n{}right={},\n{}level={}\n{}]".format(
            self.level * "\t", self.left, self.level * "\t", self.right, self.level * "\t", self.level, (self.level - 1) * "\t"
        )
        """
        if self.data is not None:
            return str(self.data)
        return "[{},{}]".format(self.left, self.right)

    def __repr__(self):
        return self.__str__()


def solve():
    numbers = []
    for line in sys.stdin:
        numbers.append(eval(line.strip()))
    magnitudes = []
    for first in numbers:
        for second in numbers:
            first_n = SnailfishNumber.parse(first, 1)
            second_n = SnailfishNumber.parse(second, 1)
            result = first_n.sum(second_n)
            result.reduce()
            magnitudes.append(result.magnitude())
    return max(magnitudes)


if __name__ == '__main__':
    print(solve())
