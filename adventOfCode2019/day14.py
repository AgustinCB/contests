import math
import sys
from collections import defaultdict
from typing import Tuple, Iterator, Dict

Ingredient = Tuple[int, str]


def parse_tree(content: Iterator[str]) -> Dict[str, Tuple[int, Dict[str, int]]]:
    tree = {}

    for line in content:
        line = line.replace("\n", "")
        recipe, ingredient = line.split(" => ")
        recipe = recipe.split(", ")
        quantity, ingredient = ingredient.split(" ")
        quantity = int(quantity)
        ingredients = {}
        for i in recipe:
            q, i = i.split(" ")
            ingredients[i] = int(q)
        tree[ingredient] = (quantity, ingredients)

    return tree


def flatten_tree(tree: Dict[str, Tuple[int, Dict[str, int]]]) -> Dict[str, Tuple[int, Dict[str, int], Dict[str, int]]]:
    flattened_tree = {}
    ore_based = set()

    def add_ingredient(ingredient: str):
        if ingredient in flattened_tree:
            return
        quantity, ingredients = tree[ingredient]
        if "ORE" in ingredients:
            ore_based.add(ingredient)
            flattened_tree[ingredient] = (quantity, ingredients, {})
            return

        leftovers = defaultdict(int)
        flattened_ingredients = defaultdict(int)
        for (ingredient_ingredient, needed_ingredient_quantity) in ingredients.items():
            add_ingredient(ingredient_ingredient)
            produced_ingredients = flattened_tree[ingredient_ingredient][0]
            if ingredient_ingredient in ore_based:
                if leftovers[ingredient_ingredient] < needed_ingredient_quantity:
                    # flattened_ingredients[ingredient_ingredient] += needed_ingredient_quantity
                    leftovers[ingredient_ingredient] += produced_ingredients - needed_ingredient_quantity
                else:
                    leftovers[ingredient_ingredient] -= needed_ingredient_quantity
                # continue
                flattened_ingredients[ingredient_ingredient] += needed_ingredient_quantity
                leftovers[ingredient_ingredient] += produced_ingredients - needed_ingredient_quantity
                continue
            for (i, q) in flattened_tree[ingredient_ingredient][1].items():
                print("ING {}: {} ({} {})".format(i, math.ceil(needed_ingredient_quantity / produced_ingredients) * q, needed_ingredient_quantity, q))
                quantity_to_consume = math.ceil(needed_ingredient_quantity / produced_ingredients) * q
                if leftovers[i] < needed_ingredient_quantity:
                    # flattened_ingredients[i] += q
                    leftovers[i] += quantity_to_consume - q
                else:
                    leftovers[i] -= q
                flattened_ingredients[i] += q
                leftovers[i] += quantity_to_consume - q
            print("{} {}".format(ingredient_ingredient, flattened_ingredients))
        flattened_tree[ingredient] = (quantity, flattened_ingredients, leftovers)

    add_ingredient("FUEL")
    return flattened_tree


"""
145 ORE => 6 MNCFX
176 ORE => 6 VJHF
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
22 VJHF, 37 MNCFX => 5 FWMGM
17 NVRVD, 3 JNWZP => 8 VPVL
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
{
  'NVRVD': (4, {'ORE': 139}, {}),
  'JNWZP': (7, {'ORE': 144}, {}),
  'VJHF': (6, {'ORE': 176}), {},
  'MNCFX': (6, {'ORE': 145}, {}),
  'VPVL': (8, {'NVRVD': 17, 'JNWZP': 3}, {'NVRVD': 3, 'JNWZP': 4}),
  'FWMGM': (5, {'VJHF': 22, 'MNCFX': 37}, {'VJHF': 2, 'MNCFX': 5}),
  'CXFTF': (8, {'NVRVD': 1}, {'NVRVD': 3}),
  'RFSQX': (4, {'VJHF': 1, 'MNCFX': 6}, {'VJHF': 5, 'MNCFX': 0}),
  'STKFG': (1, {'NVRVD': 18, 'JNWZP': 3, 'VJHF': 44, 'MNCFX': 85}, {'NVRVD': 2, 'JNWZP': 2, 'VJHF': 4, 'MNCFX': 5}),
  'HVMC': (3, {'MNCFX': 54, 'VJHF': 24, 'NVRVD': 20, 'JNWZP': 3}, {'JNWZP': 4}),
  'GNMV': (6, {'VJHF': 5, 'MNCFX': 7, 'NVRVD': 39, 'JNWZP': 6}, {'VJHF': 1, 'MNCFX': 5, 'NVRVD': 1, 'JNWZP': 1}),
  'FUEL': (1, {'NVRVD': 1698, 'JNWZP': 270, 'VJHF': 3051, 'MNCFX': 6004})
}
"""


def solve():
    ingredients = parse_tree(sys.stdin)
    flattened_tree = flatten_tree(ingredients)
    print(flattened_tree)
    if sys.argv[1] == 'part1':
        ores = 0
        _, final_ingredients, _ = flattened_tree["FUEL"]
        for (ingredient, quantity) in final_ingredients.items():
            ingredient_quantity, ingredient_ingredients, _ = flattened_tree[ingredient]
            ingredient_ores = ingredient_ingredients["ORE"]
            ores += math.ceil(quantity / ingredient_quantity) * ingredient_ores
        return ores
    if sys.argv[1] == 'part2':
        pass


if __name__ == '__main__':
    print(solve())
