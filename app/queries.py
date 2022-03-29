from db import db_session
from models import Ingredient, Cocktail, CocktailIngredient


def ingredients_in_cocktail_joined(ingredient_name):
    query = db_session.query(Cocktail).join(
        CocktailIngredient, CocktailIngredient.cocktail_id == Cocktail.id).join(Ingredient, CocktailIngredient.ingredient_id == Ingredient.id
    ).filter().all()
    cocktail_list = []
    for cocktail, ingredient in query:
            cocktail_list.append(f'{ingredient.name} - {cocktail.name}')
    return cocktail_list

