from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from flask_mail import Mail
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from celery import Celery
from flask_sse import sse
from flask_caching import Cache


app = Flask(__name__)
api = Api(app)
CORS(app)

# -------------------FLASK SSE (SERVER SIDE EVENTS)----------------------
app.register_blueprint(sse, url_prefix="/stream")




# -------------------FLASK CACHING----------------------
app.config["CACHE_TYPE"] = "SimpleCache"
# app.config["CACHE_TYPE"] = "RedisCache"
# app.config["CACHE_REDIS_HOST"] = "localhost"
# app.config["CACHE_REDIS_PORT"] = 6379
cache = Cache(app)




# -------------------LOCAL VARIABLES----------------------
filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=filepath)

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




# -------------------CELERY-----------------------------
app.config["REDIS_URL"] = "redis://localhost:6379"
CELERY_CONFIG = {"broker_url":"redis://localhost:6379/1", "result_backend":"redis://localhost:6379/2"}

celery = Celery("Groccery Store Jobs")
celery.conf.update(CELERY_CONFIG)
celery.conf.enable_utc = False


db = SQLAlchemy(app)
mail = Mail(app)

# IMPORTING ALL THE ENDPOINTS
from src.routes import auth, user, category, test, cart, product, order