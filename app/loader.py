import csv

from db import db_session
from models import Ingredient, Cocktail


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['name', 'description', 'origin']
        reader = csv.DictReader(f, fields, delimiter=';')
        ingredient_form = []
        for row in reader:
            ingredient_form.append(row)
        return ingredient_form


def save_ingredients(data):
    processed = []
    unique_ingredients = []
    for row in data:
        if row['ingredient'] not in processed:
            ingredient = {'name': row['name'], 'description': row['description'], 'origin': row['origin']}
            unique_ingredients.append(ingredient)
            processed.append(ingredient['name'])
    db_session.bulk_insert_mappings(Ingredient, unique_ingredients, return_defaults=True)
    db_session.commit()
    return unique_ingredients


def get_ingredient_by_id(ingredients, ingredient_name):
    for ingredient in ingredients:
        if ingredient['name'] == ingredient_name:
            return ingredient['id']


def save_cocktails(data, cocktails):
    processed = []
    unique_cocktails = []
    for row in data:
        if row['cocktail_name'] not in processed:
            cocktail = {'cocktail_name': row['name'], 'cocktail_description': row['description'], 
                        'cocktail_origin': row['origin', 'recipe': row['recipe'], 
                        'cocktail_id': get_ingredient_by_id(ingredients, row['ingredient'])]}
            unique_cocktails.append(cocktail)
            processed.append(cocktail['cocktail_name'])
    db_session.bulk_insert_mappings(Cocktail, unique_cocktails, return_defaults=True)
    db_session.commit()
    return unique_cocktails



def get_ingredient_by_id(ingredients, ingredient_name):
    for ingredient in ingredients:
        if ingredient['name'] == ingredient_name:
            return ingredient['id']


if __name__ == '__main__':
    all_data = read_csv('')
    ingredients = save_ingredients(all_data)
    cocktails = save_cocktails(all_data, ingredients)