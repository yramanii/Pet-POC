from pet import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    user_id = db.relationship('User', backref='user_category')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30), nullable=False)
    number = db.Column(db.Integer)
    category_name = db.Column('category_name', db.String(50), db.ForeignKey('category.name'), nullable=True)
    wishlists = db.relationship('Wishlist', backref='user', lazy=True)
    pets = db.relationship('Pet', backref='owned_pet', lazy=True)
    
    def get_token(self, expires_sec=300):
        serial = Serializer(app.config['SECRET_KEY'], expires_in=expires_sec)
        return serial.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def varify_token(token):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
#--------------------------------------------------------------------------

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    pet_type = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    user = db.Column('username', db.String(60), db.ForeignKey('user.username'), nullable=True)
    wishlists = db.relationship('Wishlist', backref='pet', lazy=True)

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    pet_id = db.Column(db.ForeignKey('pet.id'), nullable=False)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False)
    token = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.now)
