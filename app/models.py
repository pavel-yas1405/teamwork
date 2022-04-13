from app import db
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    email = db.Column(db.String(50))
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Ingredient(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(64), index=True, unique=True)
     description = db.Column(db.Text, nullable=True)
     origin = db.Column(db.String(128), index=True)
     

     def __repr__(self):
         return '<Ingredient {} {} {}'.format(self.name, self.description, self.origin)

class Cocktail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.Text, nullable=True)
    origin = db.Column (db.String(128), index=True)
    recipe = db.Column(db.Text, nullable=False)
    

    def __repr__(self):
        return '<Cocktail {} {} {} {} >'.format(self.name, self.description, self.origin, self.recipe)

class CocktailIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cocktail_id = db.Column(db.Integer, db.ForeignKey('cocktail.id', ondelete='CASCADE'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id', ondelete='CASCADE'), nullable=False)
    
    
    __table_args__ = (
    UniqueConstraint(
        'cocktail_id',
        'ingredient_id',
        name='cocktail_id_ingredient_id_unq',
    ),
)



