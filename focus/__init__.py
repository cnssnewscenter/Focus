from flask import Flask, jsonify, g
from flask.ext.login import LoginManager
from pymongo import MongoClient
import os
from .errors import APIError


app = Flask(__name__)
app.config.from_pyfile('config.py')

if "config" in os.environ and os.environ['config']:
    app.config.from_envvar("config")

loginmanager = LoginManager()

loginmanager.init_app(app)

mongodb = MongoClient(app.config['MONGO_URI'])[app.config['MONGO_DB']]


# the g object is freshed every requests , so we should add the db in it
@app.before_request
def init_g_value():
    g.mongodb = mongodb

@app.errorhandler(APIError)
def print_the_error(error):
    response = jsonify(error.to_dict())
    # return normal 200 code so we needn't deal the problem in the frontend
    return response

from . import model
from . import views
from . import admin
from . import projects
