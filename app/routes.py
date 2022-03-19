from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

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

