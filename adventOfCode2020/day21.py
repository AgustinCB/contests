import sys
from typing import Tuple, Set, List, Dict


def build_allergens_candidates(recipes: List[Tuple[Set[str], Set[str]]]) -> Dict[str, Set[str]]:
    candidates = {}
    for (ingredients, allergens) in recipes:
        for allergen in allergens:
            if allergen not in candidates:
                candidates[allergen] = ingredients
            else:
                candidates[allergen] = candidates[allergen].intersection(ingredients)
    return candidates


def parse_line(line: str) -> Tuple[Set[str], Set[str]]:
    ingredients, allergens = line.split(" (contains ")
    return set(ingredients.split(" ")), set(allergens[:-1].split(", "))


def count_non_allergic_ingredients(candidates: Dict[str, Set[str]], recipes: List[Tuple[Set[str], Set[str]]]) -> int:
    fixed = set()
    for c in candidates.values():
        fixed = fixed.union(c)
    ingredients = set()
    for (i, _) in recipes:
        ingredients = ingredients.union(i)
    not_allergic = ingredients - fixed
    return sum(len(i.intersection(not_allergic)) for (i, _) in recipes if len(i.intersection(not_allergic)) > 0)


def find_allergic_ingredients(candidates: Dict[str, Set[str]]) -> Dict[str, str]:
    allergic_ingredients = {}
    while len(allergic_ingredients) < len(candidates):
        new_ingredients = []
        for (allergen, possible_ingredients) in candidates.items():
            if allergen in allergic_ingredients:
                continue
            if len(possible_ingredients) == 1:
                allergic_ingredients[allergen] = list(possible_ingredients)[0]
                new_ingredients.append(allergic_ingredients[allergen])
        for ingredient in new_ingredients:
            for (allergen, possible_ingredients) in candidates.items():
                if allergen in allergic_ingredients:
                    continue
                candidates[allergen] = possible_ingredients - {ingredient}
    return allergic_ingredients


def solve():
    recipes = []
    for line in sys.stdin:
        recipes.append(parse_line(line.strip()))
    candidates = build_allergens_candidates(recipes)

    if sys.argv[1] == 'part1':
        return count_non_allergic_ingredients(candidates, recipes)
    if sys.argv[1] == 'part2':
        allergic_ingredients = find_allergic_ingredients(candidates)
        sorted_allergic_ingredients = sorted(allergic_ingredients.items())
        return ','.join([ingredient for (_, ingredient) in sorted_allergic_ingredients])


if __name__ == '__main__':
    print(solve())
