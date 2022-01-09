from abc import ABC, abstractmethod
import sys
from typing import List, Union, Tuple, Callable

ParserInput = List[Union[str, List[Union[str, List[str]]]]]


class Node(ABC):
    @abstractmethod
    def eval(self) -> int:
        pass


class Number(Node):
    def __init__(self, n: int):
        self.__n = n

    def eval(self) -> int:
        return self.__n

    def __str__(self) -> str:
        return str(self.__n)

    def __repr__(self) -> str:
        return self.__str__()


class Sum(Node):
    def __init__(self, n1: Node, n2: Node):
        self.__n1 = n1
        self.__n2 = n2

    def eval(self) -> int:
        return self.__n1.eval() + self.__n2.eval()

    def __str__(self) -> str:
        return "({} + {})".format(self.__n1, self.__n2)

    def __repr__(self) -> str:
        return self.__str__()


class Mul(Node):
    def __init__(self, n1: Node, n2: Node):
        self.__n1 = n1
        self.__n2 = n2

    def eval(self) -> int:
        return self.__n1.eval() * self.__n2.eval()

    def __str__(self) -> str:
        return "({} * {})".format(self.__n1, self.__n2)

    def __repr__(self) -> str:
        return self.__str__()


def lexer(line: str) -> Tuple[ParserInput, int]:
    level_stack = []
    brackets = ['(', ')']
    i = 0
    while i < len(line):
        c = line[i]
        if c == ' ':
            i += 1
            continue
        if c not in brackets:
            level_stack.append(c)
        elif c == brackets[0]:
            node, offset = lexer(line[i+1:])
            i += offset
            level_stack.append(node)
        elif c == brackets[1]:
            return list(reversed(level_stack)), i + 1
        i += 1
    return list(reversed(level_stack)), i


def lexer_to_advanced(parser_input: ParserInput) -> ParserInput:
    if len(parser_input) == 0:
        return []
    if len(parser_input) == 1 and type(parser_input[0]) == str:
        return parser_input
    elif len(parser_input) == 1:
        return [lexer_to_advanced(parser_input[0])]
    if parser_input[1] == '+':
        i = 3
        while i < len(parser_input) and parser_input[i] == '+':
            i += 2
        left_side = [lexer_to_advanced(t) if type(t) == list else t for t in parser_input[0:i]]
        return [left_side] + parser_input[i:i+1] + lexer_to_advanced(parser_input[i+1:])
    else:
        i = 3
        while i < len(parser_input) and parser_input[i] == '*':
            i += 2
        i -= 2
        left_side = [lexer_to_advanced(t) if type(t) == list else t for t in parser_input[0:i]]
        return left_side + parser_input[i:i+1] + lexer_to_advanced(parser_input[i+1:])


def parse(parser_input: ParserInput) -> Node:
    if len(parser_input) == 1 and type(parser_input[0]) == str:
        return Number(int(parser_input[0]))
    elif len(parser_input) == 1:
        return parse(parser_input[0])
    if parser_input[1] == '+':
        return Sum(parse([parser_input[0]]), parse(parser_input[2:]))
    else:
        return Mul(parse([parser_input[0]]), parse(parser_input[2:]))


def parse_operation(line: str, op: Callable[[ParserInput], ParserInput] = lambda p: p) -> Node:
    return parse(op(lexer(line)[0]))


def solve():
    if sys.argv[1] == 'part1':
        operations = []
        for line in sys.stdin:
            operations.append(parse_operation(line.strip()))

        return sum(o.eval() for o in operations)
    if sys.argv[1] == 'part2':
        operations = []
        for line in sys.stdin:
            operations.append(parse_operation(line.strip(), lexer_to_advanced))
        for o in operations:
            print(o)

        return sum(o.eval() for o in operations)


if __name__ == '__main__':
    print(solve())
