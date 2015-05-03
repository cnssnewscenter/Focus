from flask import Blueprint
from focus import app
NAME = "slide"

main = Blueprint(NAME, __name__, template_folder="templates")
app.register_blueprint(main)
main.TITLE = "多图全屏轮播"


def create_project():
    pass

main.create_project = create_project
