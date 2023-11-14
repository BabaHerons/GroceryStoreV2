from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from flask_mail import Mail
from dotenv import load_dotenv


app = Flask(__name__)
api = Api(app)
CORS(app)

filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=filepath)


# -------------------JWT PRIVATE TOKEN KEY------------------
SECRET_TOKEN_KEY = os.environ.get('SECRET_TOKEN_KEY')

# --------------------DATABASE CONNECTION-------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grocery_store_v2.db"

# -------------------SECRET KEY-----------------------------
app.config['SECRET_KEY'] = os.environ.get("APP_SECRET_KEY")

# -------------------EMAIL CONFIGURATION---------------------
# app.config['MAIL_SERVER'] = ''
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = ''
# app.config['MAIL_PASSWORD'] = ''
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_DEFAULT_SENDER'] = ''



db = SQLAlchemy(app)
mail = Mail(app)

# IMPORTING ALL THE ENDPOINTS
from src.routes import auth