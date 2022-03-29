from app import app, db
from app.forms import LoginForm
from app.models import Ingredient, Cocktail
from flask import render_template, flash, redirect, url_for, request
from urllib import response

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
    


@app.route('/ingredient/new', methods=['POST'])
def new_ingredient():
    if request.method == 'POST':
        new_ingredient = Ingredient(name=request.form['name'], description=request.form['description'], origin=request.form['origin'])
        db.session.add(new_ingredient)
        db.session.commit()
        return redirect(url_for('ingredient'))
    else:
        return render_template('new_ingredient.html')

@app.route('/ingredient', methods=['GET'])
def ingredient():
    ingredients = db.session.query(Ingredient).all()
    title = "Ингредиенты"
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
            return redirect(url_for('ingredient', cocktail_id=ingredient_id))  
    else:  
        return render_template('edit_cocktail.html', cocktail=edited_ingredient)


@app.route('/ingredient/<int:ingredient_id>/delete', methods=['GET', 'POST'])
def delete_ingredient(ingredient_id):
    ingredient_to_delete = db.session.query(Ingredient).filter_by(id=ingredient_id).one()
    if request.method == 'POST':
        db.session.delete(ingredient_to_delete)
        db.session.commit()
        return redirect(url_for('ingredient', cocktail_id=ingredient_id))
    else:
        return render_template('delete_ingredient.html', ingredient=ingredient_to_delete)


@app.route('/cocktail')
def cocktail():
    cocktails = db.session.query(Cocktail).all()
    title = "Коктейли"
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

