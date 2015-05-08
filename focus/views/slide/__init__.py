from flask import Blueprint
from focus import app
from functools import wraps
NAME = "slide"

main = Blueprint(NAME, __name__, template_folder="templates")
app.register_blueprint(main)
main.TITLE = "多图全屏轮播"

def register_action(name):


def init():

    """
    put the init task here, like create the folder or init the data
    This is a simple example, so nothing needed.
    """

    pass


@main.route("/admin/project/<proj(slide):p>/change_pics")
def pics(p):
    return "Change Pic"

actions = {
    "上传图片": pics
}
