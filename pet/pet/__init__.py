from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from pet.flask_celery import make_celery

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '<generate secret key>'
app.config['SQLALCHEMY_DATABASE_URI'] = '<database configuration>'
#----------------------------------------------------------------------------------------------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "<enter your email>"
app.config['MAIL_PASSWORD'] = "" #have to enter password
mail = Mail(app)


app.config['task_serializer'] = 'pickle'
# app.config['result_serializer'] = 'pickle'
app.config['accept_content'] = ['pickle', 'json']
app.config['SERVER_NAME'] = 'localhost:5000'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

celery = make_celery(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from pet import routes


# app.wsgi_app = token_middleware(app.wsgi_app)
# from pet.middleware import token_middleware
