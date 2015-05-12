from flask import Blueprint, render_template, send_from_directory, request
from focus import mongodb, addClick, app
import functools

NAME = "slide"
main = Blueprint(NAME, __name__, template_folder="templates")
main.TITLE = "多图全屏轮播"
main.actions = {}


def register_action(name):
    def wrapper(func):
        main.actions[name] = func

        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return func_wrapper
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
    pics = mongodb[project].find_one({"id": "pictures"}) or []
    return render_template("change_pics.html", project=project, pics=pics)


@main.route("/admin/project/<proj(slide):project>/custom_css", methods=["GET", "POST"])
@register_action('自定义 CSS')
def slide_custom_css(project):
    if request.method == 'GET':
        css = mongodb[project].find_one({"id": "css"})
        if css:
            css = css['value']
        return render_template("change_css.html", project=project, css=css)
    elif request.method == 'POST':
        css = request.form.get("css")
        mongodb[project].replace_one({'id': 'css'}, {'id': 'css', 'value': css}, True)
        return render_template("change_css.html", project=project, css=css)


@main.route("/p/<proj(slide):project>/")
@addClick
def slide_index(project):
    pics = [i.name for i in mongodb[project].find()]
    css = mongodb['project'].find_one({'id': 'css'})  # should avoid injection
    return render_template("index.html", pics=pics, css=css)


@main.route("/p/<proj(slide):project>/<path:static>")
def slide_static(project, static):
    return send_from_directory('static', static)
