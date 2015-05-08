from flask import Blueprint
from focus import app
NAME = "slide"

main = Blueprint(NAME, __name__, template_folder="templates")
app.register_blueprint(main)
main.TITLE = "多图全屏轮播"


def init():

    """
    put the init task here, like create the folder or init the data
    This is a simple example, so nothing needed.
    """

    pass

actions = []
