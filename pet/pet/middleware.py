from werkzeug.wrappers import Request, Response, ResponseStream
from functools import wraps
from flask import Response, request, jsonify, render_template, url_for, redirect
from flask_login import current_user

from pet.forms import LoginForm
from pet.models import User, Pet
import hashlib
import jwt
from datetime import datetime, timedelta
from pet import app
import json

from flask_login import current_user, login_user


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        # if request.method == 'POST':
            # breakpoint()
        token = None
        if 'tokens' in request.headers:
            token = request.headers['tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(email=data['name']).first()
            login_user(current_user)
        except:
            return jsonify({'message': 'token is invalid'})

        return f(*args, **kwargs)
    return decorator


# class token_middleware():

#     def __init__(self, app):
#         self.app = app

#     def __call__(self, environ, start_response):
#         breakpoint()
        
#         request = Request(environ)
#         # with app.app_context():
#         email = request.authorization['username']
#         password = request.authorization['password']
#         user = User.query.filter_by(email=email, password=password).first()

#         if user:
#             return self.app(environ, start_response)


#         res = Response('Authentication failed.', mimetype='text/plain', status=401)
#         return res(environ, start_response)

class token_middleware():

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # breakpoint()
        
        req = Request(environ)

        with app.app_context():
            # breakpoint()
            if req.method=='GET' and req.path=='/login':
                pass
            elif req.method=='POST' and req.path=='/api/login':
                pass
            elif req.method=='POST' and req.path=='/login':
                pass
            elif req.method=='GET' and req.path=='/logout':
                pass
            elif req.method=='GET' and req.path=='/register':
                pass
            elif req.method=='POST' and req.path=='/register':
                pass
            elif req.method=='GET' and req.path=='/':
                pass
            elif req.method=='GET' and req.path=='/favicon.ico':
                pass
            elif req.method=='GET' and req.path=='/dashboard':
                pass
            elif req.method=='GET' and req.path=='/pet':
                pass
            elif req.method=='POST' and req.path=='/pet':
                pass
            else:
                token = req.headers['tokens']

                if not token:
                    return jsonify({"Message":"A valid token is missing."})
                try:
                    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                    user = User.query.filter_by(email=data['name']).first()
                    # if user:
                    # login_user(user)
                except:
                    return jsonify({"Message":"Enter a Valid Token."})
                
            
            return self.app(environ, start_response)    #this line redirects to login when login request is sent.


        # res = Response('Authentication failed.', mimetype='text/plain', status=401)
        return Response(environ, start_response)



# after authentiaction of user,
# create a New Table:
# token, email, login-time/created date
# token exppires after some time

























# def login_middleware(func):
#     @wraps(func)
#     def decorated_function(*args, **kwargs):
#         # breakpoint()
#         login_from = LoginForm()
#         input_email = login_from.email.data
#         input_pass = login_from.password.data
#         user = User.query.filter_by(email=input_email, password=input_pass).first()
#         if user:
            
#             return func(*args, **kwargs)

#         return Response('Authorization failed', mimetype='text/plain', status=401)

#     return decorated_function