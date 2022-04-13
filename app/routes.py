import json
import requests
from flask import render_template, flash, redirect, url_for, request
from app import app
from app import db
from flask_login import LoginManager, login_user, logout_user, current_user
from app.models import Cocktail, Ingredient, User
from decorators import admin_required
from app.forms import LoginForm, RegistrationForm


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
@app.route('/index')
def index():
    title = "Карта коктейлей"
    return render_template('index.html', title=title)


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template('login.html', title=title, form=login_form)


@app.route('/process_login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            login_user(user)
            flash('Вы успешно вошли на сайт')
            return redirect(url_for('index'))

    flash('Неправильные имя или пароль')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('index'))


@app.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    title = "Регистрация"
    return render_template('registration.html', title=title, form=form)


@app.route('/process_reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле {}: {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
        return redirect(url_for('register'))


@app.route('/admin')
@admin_required
def admin_index():
    title = "Панель управления"
    return render_template('admin.html', title=title)


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



