from urllib import response
from flask import render_template, flash, redirect, url_for, json, request
from app import app
from app.forms import LoginForm, SearchForm
from app import db
from app.models import Cocktail


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


@app.route('/create_cocktail', methods=['POST'])

def create_cocktail():
    request_data = json.loads(request.data)
    name = request_data['name']
    description = request_data['description']
    origin = request_data['origin']
    recipe = request_data['recipe']

    new_cocktail = Cocktail(
        name=name,
        description=description,
        origin=origin,
        recipe=recipe
    )

    db.session.add(new_cocktail)
    db.session.commit()

    response = app.response_class(
        response=json.dumps({'result_info': 'Запись ингредиента создана'}),
        mimetype='application/json'
    )
    return response 

@app.route('/cocktail')
def cocktail():
    cocktails = db.session.query(Cocktail).all()
    return render_template('cocktail.html', cocktails=cocktails)

@app.route('/cocktail/new', methods=['GET', 'POST'])
def newCocktail():
    if request.method == 'POST':
        newCocktail = Cocktail(name=request.form['name'], description=request.form['description'], origin=request.form['origin'], recipe=request.form['recipe'])
        db.session.add(newCocktail)
        db.session.commit()
        return redirect(url_for('cocktail'))
    else:
        return render_template('newCocktail.html')

@app.route("/cocktail/<int:cocktail_id>/edit/", methods=['GET', 'POST'])  
def editCocktail(cocktail_id):  
    editedCocktail = db.session.query(Cocktail).filter_by(id=cocktail_id).one()  
    if request.method == 'POST':  
        if request.form['name']:  
            editedCocktail.name = request.form['name']
            editedCocktail.description = request.form['description']
            editedCocktail.origin = request.form['origin']
            editedCocktail.recipe = request.form['recipe']
            db.session.add(editedCocktail)
            db.session.commit() 
            return redirect(url_for('cocktail', cocktail_id=cocktail_id))  
    else:  
        return render_template('editCocktail.html', cocktail=editedCocktail)

@app.route('/cocktail/<int:cocktail_id>/delete', methods=['GET', 'POST'])
def deleteCocktail(cocktail_id):
    cocktailToDelete = db.session.query(Cocktail).filter_by(id=cocktail_id).one()
    if request.method == 'POST':
        db.session.delete(cocktailToDelete)
        db.session.commit()
        return redirect(url_for('cocktail', cocktail_id=cocktail_id))
    else:
        return render_template('deleteCocktail.html', cocktail=cocktailToDelete)



    
    
