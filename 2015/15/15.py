import math
from collections.abc import Callable, Iterator
from dataclasses import dataclass

from utils.parsing import parse_input


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def parse_ingredients() -> list[Ingredient]:
    res = []
    for line in parse_input():
        line = line.replace(",", "")
        (
            name,
            _,
            capacity,
            _,
            durability,
            _,
            flavor,
            _,
            texture,
            _,
            calories,
        ) = line.split()
        res.append(
            Ingredient(
                name=name.rstrip(":"),
                capacity=int(capacity),
                durability=int(durability),
                flavor=int(flavor),
                texture=int(texture),
                calories=int(calories),
            )
        )
    return res


def evaluate(
    recipe: list[tuple[Ingredient, int]],
    validate_recipe: Callable[[list[tuple[Ingredient, int]]], bool] | None = None,
) -> int:
    if validate_recipe and not validate_recipe(recipe):
        return 0

    score = [0, 0, 0, 0]
    for ingredient, quantity in recipe:
        score[0] += ingredient.capacity * quantity
        score[1] += ingredient.durability * quantity
        score[2] += ingredient.flavor * quantity
        score[3] += ingredient.texture * quantity
    return math.prod([0 if s <= 0 else s for s in score])


def iterate(ingredients: list[Ingredient]) -> Iterator[list[tuple[Ingredient, int]]]:
    def _inner(
        recipe: list[tuple[Ingredient, int]],
        remaining_ingredients: list[Ingredient],
        total: int,
    ) -> Iterator[list[tuple[Ingredient, int]]]:
        if total == 100:
            yield recipe
            return
        elif len(remaining_ingredients) == 1:
            recipe = [*recipe, (remaining_ingredients[0], 100 - total)]
            yield recipe
            return

        ingredient = remaining_ingredients[0]
        for i in range(100 - total + 1):
            new_recipe = [*recipe]
            if i > 0:
                new_recipe.append((ingredient, i))
            yield from _inner(new_recipe, remaining_ingredients[1:], total + i)

    yield from _inner([], ingredients, 0)


def main1() -> int:
    ingredients = parse_ingredients()
    return max(evaluate(recipe) for recipe in iterate(ingredients))


def main2() -> int:
    ingredients = parse_ingredients()

    def validate_recipe(recipe: list[tuple[Ingredient, int]]) -> bool:
        return (
            sum(ingredient.calories * quantity for ingredient, quantity in recipe)
            == 500
        )

    return max(evaluate(r, validate_recipe) for r in iterate(ingredients))
