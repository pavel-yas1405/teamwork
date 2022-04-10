import json
import requests
from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from app import db
from app.models import Cocktail, Ingredient


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
    

@app.route('/create_ingredient', methods=['POST'])
def create_ingredient():
    name = name
    description = description
    origin = origin

    db.session.add(ingredient)
    db.session.commit()
    return render_template(page_title=name, description=description, origin=origin)

@app.route('/ingredient')
def ingredient_id():
    return Ingredient.query.get(ingredient_id)


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



