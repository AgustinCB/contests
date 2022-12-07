from __future__ import annotations
import sys
from typing import Iterable, List, Tuple, Optional


File = Tuple[int, str]


directories = []


class Directory(object):
    def __init__(self, name: str, parent: Optional[Directory]):
        self.name = name
        self.files = []
        self.directories = {}
        self.parent = parent
        self.dir_size = -1
        directories.append(self)

    def size(self):
        if self.dir_size == -1:
            self.dir_size = sum(s for s, _ in self.files) + sum(d.size() for d in self.directories.values())
        return self.dir_size

    def __str__(self) -> str:
        return ("- {} from {} (size {})" +
                "  {}\n" +
                "\n".join([str(d) for d in self.directories.values()])
        ).format(self.name, self.parent.name if self.parent is not None else "None", self.size(), " ".join("({} {})".format(s, n) for s,n in self.files))

    def __repr__(self):
        return str(self)


def parse_dir_entry(line: str, current_dir: Directory):
    parts = line.split(" ")
    if parts[0].isnumeric():
        current_dir.files.append((int(parts[0]), parts[1]))
    else:
        current_dir.directories[parts[1]] = Directory(parts[1], current_dir)


def parse_cd(line: str, current_dir: Directory, root: Directory) -> Directory:
    dst = line.replace("$ cd ", "")
    if dst == "..":
        return current_dir.parent
    elif dst == "/":
        return root
    else:
        return current_dir.directories[dst]


def parse_ls(input_stream: Iterable[str], current_dir: Directory, root: Directory) -> Directory:
    for line in input_stream:
        if line.startswith("$"):
            return parse_cd(line.strip(), current_dir, root)
        parse_dir_entry(line.strip(), current_dir)


def parse(input_stream: Iterable[str], root: Directory):
    current_dir = root
    for line in input_stream:
        if line.startswith("$ ls"):
            current_dir = parse_ls(input_stream, current_dir, root)
        else:
            current_dir = parse_cd(line.strip(), current_dir, root)


def solve():
    sys.stdin.readline()
    root = Directory("/", None)
    parse(sys.stdin, root)
    sizes = [d.size() for d in directories]
    if sys.argv[1] == 'part1':
        return sum(s for s in sizes if s < 100000)
    if sys.argv[1] == 'part2':
        used_space = root.size()
        free_space = 70000000 - used_space
        required_space_to_delete = 30000000 - free_space
        return min(s for s in sizes if s >= required_space_to_delete)


if __name__ == '__main__':
    print(solve())
