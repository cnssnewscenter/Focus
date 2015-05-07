from flask import Flask, jsonify, render_template
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


@app.errorhandler(APIError)
def print_the_error(error):
    response = jsonify(error.to_dict())
    # return normal 200 code so we needn't deal the problem in the frontend
    return response


@app.errorhandler(404)
def Page_not_find(error):
    return render_template('404.html')


from . import model
from . import views
from . import admin
from . import projects
