from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm
from app.models import Cocktail, Ingredient, Origin
from re import search
import requests, json, string

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])

def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
        
    return render_template('login.html', title='Sign In', form=form)    
    

@app.route('/ingredient/new', methods=['GET','POST'])

def new_ingredient():
    if request.method == 'POST':
        new_ingredient = Ingredient(name=request.form['name'], description=request.form['description'], origin=request.form['origin'])
        db.session.add(new_ingredient)
        db.session.commit()
        return redirect(url_for('ingredient'))
    else:
        return render_template('new_ingredient.html')

@app.route('/ingredient')
def ingredient():
     ingredients = db.session.query(Ingredient).all()
     title = "Ингредиенты"

     q = request.args.get('q')

     if q:
         ingredients = Ingredient.query.filter(Ingredient.name.contains(q) | Ingredient.description.contains(q)).all()
     else:
         ingredients = Ingredient.query.all()
     return render_template('ingredient.html', ingredients=ingredients, title=title)


@app.route("/ingredient/<int:ingredient_id>/edit/", methods=['GET', 'POST'])  
def edit_ingredient(ingredient_id):  
    edited_ingredient = db.session.query(Ingredient).filter_by(id=ingredient_id).one()  
    if request.method == 'POST':  
        if request.form['name']:  
            edited_ingredient.name = request.form['name']
            edited_ingredient.description = request.form['description']
            edited_ingredient.origin = request.form['origin']
            db.session.add(edited_ingredient)
            db.session.commit() 
            return redirect(url_for('ingredient', ingredient_id=ingredient_id))  
    else:  
        return render_template('edit_ingredient.html', ingredient=edited_ingredient)

@app.route('/ingredient/<int:ingredient_id>/delete', methods=['GET', 'POST'])
def delete_ingredient(ingredient_id):
    ingredient_to_delete = db.session.query(Ingredient).filter_by(id=ingredient_id).one()
    if request.method == 'POST':
        db.session.delete(ingredient_to_delete)
        db.session.commit()
        return redirect(url_for('ingredient', ingredient_id=ingredient_id))
    else:
        return render_template('delete_ingredient.html', ingredient=ingredient_to_delete)
    

@app.route('/parser_ingredient', methods=['POST'])
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
        return render_template(new_ingredients)



@app.route('/cocktail')
def cocktail():
     cocktails = db.session.query(Cocktail).all()
     title = "Коктейли"

     q = request.args.get('q')

     if q:
         cocktails = Cocktail.query.filter(Cocktail.name.contains(q) | Cocktail.description.contains(q)).all()
     else:
         cocktails = Cocktail.query.all()
     return render_template('cocktail.html', cocktails=cocktails, title=title)



@app.route('/cocktail/new', methods=['GET', 'POST'])
def new_cocktail():
     if request.method == 'POST':
         new_cocktail = Cocktail(name=request.form['name'], description=request.form['description'], origin=request.form['origin'], recipe=request.form['recipe'])
         db.session.add(new_cocktail)
         db.session.commit()
         return redirect(url_for('cocktail'))
     else:
         return render_template('new_cocktail.html')


@app.route('/parse_cocktail', methods=['POST'])
def change_url():
    existed_cocktails=[x.name for x in db.session.query(Cocktail).all()]
    alph = list(string.ascii_lowercase)
    default_url = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?f={}'
    new_cocktails = []
    for letter in alph:
        new_url = default_url.format(letter)
        cocktail_dict = requests.get(new_url).json()
        drinks = cocktail_dict.get('drinks')
        if not drinks:
            print('NO COCKTAIL AVAILABLE FOR THIS LETTER')
            continue
        for cocktail in drinks:
            cocktail_name = cocktail['strDrink']
            if cocktail_name not in existed_cocktails:
                cocktail_recipe = cocktail['strInstructions']
                new_cocktail = Cocktail(name=cocktail_name, recipe=cocktail_recipe, origin_id=1)
                new_cocktails.append(new_cocktail)
    db.session.bulk_save_objects(new_cocktails)
    db.session.commit()
    return new_cocktails



@app.route("/cocktail/<int:cocktail_id>/edit/", methods=['GET', 'POST'])  
def edit_cocktail(cocktail_id):  
    edited_cocktail = db.session.query(Cocktail).filter_by(id=cocktail_id).one()  
    if request.method == 'POST':  
        if request.form['name']:  
            edited_cocktail.name = request.form['name']
            edited_cocktail.description = request.form['description']
            edited_cocktail.origin = request.form['origin']
            edited_cocktail.recipe = request.form['recipe']
            db.session.add(edited_cocktail)
            db.session.commit() 
            return redirect(url_for('cocktail', cocktail_id=cocktail_id))  
    else:  
        return render_template('edit_cocktail.html', cocktail=edited_cocktail)


@app.route('/cocktail/<int:cocktail_id>/delete', methods=['GET', 'POST'])
def delete_cocktail(cocktail_id):
    cocktail_to_delete = db.session.query(Cocktail).filter_by(id=cocktail_id).one()
    if request.method == 'POST':
        db.session.delete(cocktail_to_delete)
        db.session.commit()
        return redirect(url_for('cocktail', cocktail_id=cocktail_id))
    else:
        return render_template('delete_cocktail.html', cocktail=cocktail_to_delete)


@app.route('/origin')
def origin():
     origins = db.session.query(Origin).all()
     title = "Родина коктейля"

     q = request.args.get('q')

     if q:
         origins = Origin.query.filter(Origin.country.contains(q) | Origin.region.contains(q)).all()
     else:
         origins = Origin.query.all()
     return render_template('origin.html', origins=origins, title=title)


@app.route('/origin/new', methods=['GET','POST'])
def new_origin():
    if request.method == 'POST':
        new_origin = Origin(country=request.form['country'], region=request.form['region'])
        db.session.add(new_origin)
        db.session.commit()
        return redirect(url_for('origin'))
    else:
        return render_template('new_origin.html')

        
@app.route("/origin/<int:origin_id>/edit/", methods=['GET', 'POST'])  
def edit_origin(origin_id):  
    edited_origin = db.session.query(Origin).filter_by(id=origin_id).one()  
    if request.method == 'POST':  
        if request.form['name']:  
            edited_origin.country = request.form['country']
            edited_origin.region = request.form['region']
            db.session.add(edited_origin)
            db.session.commit() 
            return redirect(url_for('origin', origin_id=origin_id))  
    else:  
        return render_template('edit_origin.html', origin=edited_origin)

@app.route('/origin/<int:origin_id>/delete', methods=['GET', 'POST'])
def delete_origin(origin_id):
    origin_to_delete = db.session.query(Origin).filter_by(id=origin_id).one()
    if request.method == 'POST':
        db.session.delete(origin_to_delete)
        db.session.commit()
        return redirect(url_for('origin', origin_id=origin_id))
    else:
        return render_template('delete_origin.html', origin=origin_to_delete)
