from flask import Blueprint, render_template, send_from_directory, request, abort, jsonify
from focus import mongodb, addClick, app
import functools
import os

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


@main.route("/admin/project/<proj(slide):project>/change_pics", methods=['GET', 'POST', 'DELETE', "PUT"])
@register_action('图片管理')
def slide_pictures_management(project):
    if request.method == 'GET':
        pics = list(sorted(mongodb[project]['pictures'].find(), key=lambda x: x.get('order', 0)))
        return render_template("change_pics.html", project=project, pics=pics)
    elif request.method == 'PUT':
        info = request.form.get('info')
        pic = request.form['fid']
        app.logger.info('Add a pic')
        pics = mongodb[project]['pictures'].insert_one({"order": mongodb[project]['pictures'].count() + 1, 'info': info, 'file': pic})
        return jsonify(err=0)
    elif request.method == 'DELETE':
        pic = request.form.get('fid')
        app.logger.info('delete a pic')
        pics = mongodb[project]['pictures'].delete_one({"file": pic})
        return jsonify(err=0)
    elif request.method == 'POST':
        pic = request.form.get('fid')
        info = request.form.get('info', '')
        order = int(request.form.get('order', '0'))
        raw = mongodb[project]["pictures"].find_one({"file": pic})
        if not raw:
            abort(400)
        if info:
            raw['info'] = info
        if order > 0 and raw['order'] != order and order <= mongodb[project].pictures.count():
            mongodb[project].pictures.update_one({'order': order}, {"$set": {"order": raw['order']}})
            raw['order'] = order

        mongodb[project].pictures.replace_one({'file': pic}, raw)
        return jsonify(err=0)


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
    title = mongodb.meta.find_one({"hmac": project}).get('title')
    pics = [i.name for i in mongodb[project].find()]
    css = mongodb[project].find_one({'id': 'css'})  # should avoid injection
    return render_template("index.html", pics=pics, css=css, title=title)


@main.route("/p/<proj(slide):project>/<path:static>")
def slide_static(project, static):
    return send_from_directory(os.path.join(os.path.split(__file__)[0], 'static'), static)


