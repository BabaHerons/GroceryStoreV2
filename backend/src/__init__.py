from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from flask_mail import Mail
from dotenv import load_dotenv
from cryptography.fernet import Fernet


app = Flask(__name__)
api = Api(app)
CORS(app)

filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=filepath)

# key = Fernet.generate_key()

# FOR PASSWORD ENCRYPTION
FERNET_KEY = bytes(os.environ.get('FERNET_KEY'), "utf-8")
fernet = Fernet(FERNET_KEY)

# -------------------JWT PRIVATE TOKEN KEY------------------
SECRET_TOKEN_KEY = os.environ.get('SECRET_TOKEN_KEY')

# --------------------DATABASE CONNECTION-------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grocery_store_v2.db"

# -------------------SECRET KEY-----------------------------
app.config['SECRET_KEY'] = os.environ.get("APP_SECRET_KEY")

# -------------------EMAIL CONFIGURATION---------------------
app.config['MAIL_SERVER'] = os.environ.get("MAIL_SERVER")
app.config['MAIL_PORT'] = os.environ.get("MAIL_PORT")
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_USERNAME")



db = SQLAlchemy(app)
mail = Mail(app)

# IMPORTING ALL THE ENDPOINTS
from src.routes import auth, user, category