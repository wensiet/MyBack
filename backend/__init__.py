# FastAPI
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
# Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Auth class, created by wensiet
# from auth import Auth

app = FastAPI()
flask_app = Flask(__name__)
app.mount('/', WSGIMiddleware(flask_app))
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
flask_app.config['SECRET_KEY'] = 'ABOBUS'  # TODO hide secret key in envs
db = SQLAlchemy(flask_app)
manager = LoginManager(flask_app)

from backend import routes, models
