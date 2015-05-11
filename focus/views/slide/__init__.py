from flask import Blueprint
from focus import app
from functools import wraps
NAME = "slide"

main = Blueprint(NAME, __name__, template_folder="templates")
app.register_blueprint(main)
main.TITLE = "多图全屏轮播"
actions = {}

def register_action(name): 
    def wrapper(func):
        actions[name] = func
        def do(*args, **kwargs):
            return func(*args, **kwargs)

        do.__name__ = func.__name__
        # recover the func name
        return do
    return wrapper


def init():

    """
    put the init task here, like create the folder or init the data
    This is a simple example, so nothing needed.
    """

    pass


@main.route("/admin/project/<proj(slide):project>/change_pics")
@register_action('图片管理')
def pictures_management(project):
    return "Change Pic of " + p
