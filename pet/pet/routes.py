import re
from flask import render_template, url_for, redirect, flash, request, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from flask.views import MethodView
import flask_login
from kombu.log import Log
from werkzeug.wrappers.response import Response

from pet import app, db, mail, celery
from flask_mail import Message

from pet.models import User, Pet, Wishlist, Token
from pet.forms import PetForm, RegistrationForm, LoginForm, ResetPasswordForm, ResetForm

from pet.middleware import token_required

import datetime

import hashlib, jwt
import json
#-------------------------------------------------------------------------------------------------------------------------
# home page
def home():
    pet = Pet.query.all()[::-1]
    return render_template("home.html", pets=pet)
app.add_url_rule('/', view_func=home, methods=['GET'])
app.add_url_rule('/', view_func=home, methods=['POST'])

# pet page
class getPet(MethodView):
    def get(self):
        pet_form = PetForm()
        return render_template('pet.html', form=pet_form)

class addPet(MethodView):
    def post(self):
        # breakpoint()
        new_pet = Pet(
            name = request.form['pet_name'],
            pet_type = request.form['pet_type'],
            age = request.form['age'],
            user = current_user.username
        )
        db.session.add(new_pet)
        db.session.commit()

        return redirect(url_for('home'))

app.add_url_rule('/pet', view_func=getPet.as_view('getpet'))
app.add_url_rule('/post/pet', view_func=addPet.as_view('addpet'))

# register page
class getRegister(MethodView):
    def get(self):
        register_form = RegistrationForm()
        return render_template('register.html', form=register_form)

class postRegister(MethodView):
    def post(self):
        breakpoint()
        new_user  = User(
            name = request.form['name'],
            number = request.form['number'],
            category_name = request.form['category'],
            username = request.form['username'],
            email = request.form['email'],
            password = request.form['password'],
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

app.add_url_rule('/register', view_func=getRegister.as_view('getregister'))
app.add_url_rule('/post/register', view_func=postRegister.as_view('postregister'))

# login page
class GetLogin(MethodView):
    def get(self):
        login_form = LoginForm()
        return render_template("login.html", form=login_form)

class PostLogin(MethodView):
    def post(self):
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Please check your email or password', 'danger')
            return redirect(url_for('login'))

app.add_url_rule('/login', view_func=GetLogin.as_view('login'))
app.add_url_rule('/post/login', view_func=PostLogin.as_view('postlogin'))

# wishlist page
class GetWishlist(MethodView):
    def get(self):
        data = Wishlist.query.filter_by(user_id=current_user.id).all()
        pet_list = [Pet.query.filter_by(id=d.pet_id).first() for d in data]
        return render_template('wishlist.html', view_data=pet_list)

class PostWishlist(MethodView):
    def post(self):
        id = request.form["data"]
        pet = Pet.query.filter_by(id=id).first()
        wishlist = Wishlist(user_id=current_user.id, pet_id=pet.id)
        db.session.add(wishlist)
        db.session.commit()
        
        return render_template('wishlist.html', pet=pet)

app.add_url_rule('/wishlist', view_func=GetWishlist.as_view('wishlist'))
app.add_url_rule('/post/wishlist', view_func=PostWishlist.as_view('postwishlist'))

# logout
class Logout(MethodView):
    def get(self):
        logout_user()
        return redirect(url_for('home'))
app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
#-------------------------------------------------------------------------------------------------------------------------
# mail sending function
@celery.task(name='pet.send_mail')
def send_mail(user):
    token = user.get_token()
    message = Message('Password Reset Request', recipients=[user.email], sender='yash@gmail.com')
    message.body=f'''
    To reset your password please follow the link below.

    {url_for('reset_token', token=token, _extarnal=True)}

    '''
    mail.send(message)

@app.route('/pass_reset', methods=['GET', 'POST'])
def ResetPassword():
    pass_reset_form = ResetPasswordForm()
    if pass_reset_form.validate_on_submit():
        user = User.query.filter_by(email=pass_reset_form.email.data).first()
        if user:
            send_mail.delay(user)
            flash('Reset mail sent.', 'success')
            return redirect(url_for('login'))
    return render_template("pass_reset.html", form=pass_reset_form)


@app.route('/pass_reset/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = User.varify_token(token)
    if user is None:
        flash('try again', 'warning')
        return redirect(url_for('reset_token'))

    form = ResetForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Password changed.')
        return redirect(url_for('login'))
#----------------------------------------------------------------------------------------------------------------
# email hasing (optional)
@app.route('/email', methods=['GET'])
def encrypt_email():
    str = 'ramaniyash19@gmail.com'
    token = hashlib.sha256(str.encode()).hexdigest()
    return "token: "+token
#----------------------------------------------------------------------------------------------------------------
