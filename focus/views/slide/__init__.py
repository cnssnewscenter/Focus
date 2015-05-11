from flask import Blueprint, render_template, send_from_directory
from focus import mongodb

NAME = "slide"
main = Blueprint(NAME, __name__, template_folder="templates")
main.TITLE = "多图全屏轮播"
main.actions = {}


def register_action(name):
    def wrapper(func):
        main.actions[name] = func

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
def slide_pictures_management(project):
    return "Change Pic of " + project


@main.route("/p/<proj(slide):project>/")
def slide_index(project):
    pics = mongodb[project].find("pictures")
    return render_template("index.html", pics=pics)


@main.route("/p/<proj(slide):project>/<path:static>")
def slide_static(project, static):
    return send_from_directory('static', static)
