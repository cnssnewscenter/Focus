from flask import Flask
from flask.ext.login import LoginManager, current_user
from pymongo import MongoClient
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')

if "config" in os.environ and os.environ['config']:
    app.config.from_envvar("config")

loginmanager = LoginManager()

loginmanager.init_app(app)

mongodb = MongoClient(app.config['MONGO_URI'])[app.config['MONGO_DB']]


from . import model
from . import views
from . import admin
from . import projects
# register the blueprints
# app.register_blueprint(admin)
