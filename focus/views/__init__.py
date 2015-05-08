from flask import Blueprint
from focus import app, mongodb
from . import slide
app.register_blueprint(slide.main)
# register all the blueprint here
