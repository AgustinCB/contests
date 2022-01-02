import sys
from typing import Set


class TestCase(object):
    def __init__(self, pokemons: Set[str], maze: str):
        self.pokemons = pokemons
        self.maze = maze

    def findPokemon(self, pokemon) -> bool:
        if pokemon in self.maze:
            self.maze = self.maze.replace(pokemon, '')
            return True
        return False

    def solve(self):
        while len(self.pokemons) > 0:
            ps = self.pokemons.copy()
            for p in ps:
                if self.findPokemon(p) or self.findPokemon("".join(reversed(p))):
                    self.pokemons.remove(p)


def parse_case() -> TestCase:
    (n_pokemons, height, width) = [int(c) for c in sys.stdin.readline().strip().split(" ")]
    pokemons = set()
    for _ in range(n_pokemons):
        pokemons.add(sys.stdin.readline().strip())
    maze = ""
    for _ in range(height):
        maze += sys.stdin.readline().strip()
    return TestCase(pokemons, maze.replace(" ", ""))


def solve():
    tests = int(sys.stdin.readline().strip())
    for test in range(tests):
        test_case = parse_case()
        test_case.solve()
        print("Case #{}: {}".format(test + 1, test_case.maze))


if __name__ == '__main__':
    solve()

