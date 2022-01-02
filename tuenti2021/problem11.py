import sys
from typing import Dict, List


class TrieNode:
    def __init__(self, value):
        self.children = {}
        self.value = value
        self.counter = 0
        self.end_of_string = False

    def get_weights_bigger_than(self, path: List[object], result: Dict[str, int], limit: int) -> Dict[str, int]:
        def update_result():
            s = ""
            to_set = limit * (self.counter // limit)
            for p in path:
                if p.value is not None:
                    p.counter -= to_set
                    s += p.value
            result[s] = to_set
        next_eligible_characters = [v for v in self.children.values() if v.counter >= limit]
        if len(next_eligible_characters) == 0:
            update_result()
        else:
            for n in next_eligible_characters:
                n.get_weights_bigger_than(path + [n], result, limit)
            if self.counter >= limit:
                update_result()
        return result


class Trie:
    def __init__(self):
        self.root = TrieNode(None)

    def insert(self, word: str):
        current = self.root
        for ch in word:
            node = current.children.get(ch)
            if node is None:
                node = TrieNode(ch)
                current.children.update({ch: node})
            node.counter += 1
            current = node
        current.end_of_string = True

    def get_weights_bigger_than(self, limit: int) -> Dict[str, int]:
        return self.root.get_weights_bigger_than([], {}, limit)


def parse_trie() -> (Trie, int):
    functions, functions_per_file = [int(c) for c in sys.stdin.readline().strip().split(" ")]
    trie = Trie()
    t = 0
    for _ in range(functions):
        f = sys.stdin.readline().strip()
        t += len(f)
        trie.insert(f)
    return trie, functions_per_file, t


def solve():
    tests = int(sys.stdin.readline().strip())
    for test in range(tests):
        trie, functions_per_file, t = parse_trie()
        result = trie.get_weights_bigger_than(functions_per_file)
        total = int(sum([
            len(prefix) * (occurrences / functions_per_file)
            for prefix, occurrences
            in result.items()
        ]))
        if functions_per_file == 1:
            total = t
        print("Case #{}: {}".format(test + 1, total))


if __name__ == '__main__':
    solve()

