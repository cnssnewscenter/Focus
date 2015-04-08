from flask import Flask
from flask.ext.login import LoginManager, current_user

app = Flask(__name__)
loginmanager = LoginManager()

loginmanager.init_app(app)
# loading the config

app.config.from_pyfile('config.py')
# app.config.from_envvar('CONFIG')


from . import model
from . import views
from . import admin
# register the blueprints
# app.register_blueprint(admin)
