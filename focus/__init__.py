from flask import Flask

app = Flask(__name__)

# loading the config

app.config.from_pyfile('config.py')
# app.config.from_envvar('CONFIG')

from . import model
from . import views
from . import admin

