import math
import sys
from collections import defaultdict
from typing import Tuple, Iterator, Dict


Ingredient = Tuple[int, str]
Recipes = Dict[str, Tuple[int, Dict[str, int]]]


def parse_tree(content: Iterator[str]) -> Recipes:
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


def calculate_fuel(
        recipe: str,
        quantity: int,
        recipes: Recipes,
        leftovers: Dict[str, int]
    ) -> int:
    if recipe in leftovers and leftovers[recipe] >= quantity:
        # print("USING LEFT OVERS", recipe, leftovers, quantity)
        leftovers[recipe] -= quantity
        return 0

    recipe_spawn, recipe_ingredients = recipes[recipe]

    # print(recipe, leftovers)
    quantity -= leftovers[recipe]
    leftovers[recipe] = 0

    if "ORE" in recipe_ingredients and len(recipe_ingredients) == 1:
        recipes_to_make = math.ceil(quantity / recipe_spawn)
        produced = recipes_to_make * recipe_spawn
        leftovers[recipe] += produced - quantity
        return recipe_ingredients["ORE"] * recipes_to_make

    fuel = 0
    for (recipe_ingredient, recipe_ingredient_quantity) in recipe_ingredients.items():
        fuel += calculate_fuel(recipe_ingredient,
            recipe_ingredient_quantity * quantity, recipes, leftovers)
        print("[{}] {} {}: {} (leftovers {})".format(quantity, recipe_ingredient_quantity, recipe_ingredient, fuel, leftovers))
    return fuel


def solve():
    ingredients = parse_tree(sys.stdin)
    if sys.argv[1] == 'part1':
        return calculate_fuel("FUEL", 1, ingredients, defaultdict(int))
    if sys.argv[1] == 'part2':
        pass


if __name__ == '__main__':
    print(solve())
