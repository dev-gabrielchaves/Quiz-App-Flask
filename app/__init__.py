from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='templates', static_folder='static')
# Do not forget that is necessary to set a secret key to your application, even in order to work
app.config['SECRET_KEY'] = '0d2ea4d89c7e62f1033f624946b07752'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db = SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)

from app import routes