import requests
import json
from app import db
from app.models import Ingredient

def get_ingredient():
    url = "https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list"
    request = requests.get(url)
    data = request.text
    ingredient = json.loads(data)
    new_ingredients = []
    for item in ingredient['drinks']:
        item['name'] = item.pop('strIngredient1')
        drink_name = item['name']
        default_url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?i={}"
        new_url = default_url.format(drink_name)
        ingredient_dict = requests.get(new_url).json()
        for item in ingredient_dict['ingredients']:
            ingredient_name = item['strIngredient']
            description = item['strDescription']
            origin = 'Неизвестно'
            new_ingredient = Ingredient(name=ingredient_name, description=description, origin=origin)
            new_ingredients.append(new_ingredient)

    db.session.bulk_save_objects(new_ingredients)
    db.session.commit()


if __name__ == "__main__":
    get_ingredient()