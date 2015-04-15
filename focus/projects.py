from flask import Flask, request, render_template, redirect, url_for, jsonify
from focus.errors import *
from focus import loginmanager, app, mongodb
from flask.ext.login import current_user, login_required, login_user, logout_user
from datetime import datetime
import pickle
import hmac


@app.route("/admin/projects")
def project_management():
    return ""


@app.route("/admin/api/project", defaults={"number": None})
@app.route("/admin/api/project/<project>")
# @login_required
def project_operation(project):
    if project:
        # return the info of single project
        pass
    else:
        # return general infomation
        pass


def validType(type_name):
    if type_name in ["a", 'b', 'c']:
        return type_name
    else:
        raise WrongPostData(1, "错误的参数")


@app.route("/admin/api/new", methods=["POST"])
def new_project_api():
    data = {
        "project_type": validType(request.form['project']),
        "comment": request.form.get('comment', ''),
        "time": datetime.now(),
        "name": request.form['name']
    }
    data['hmac'] = hmac.new(pickle.dumps(data)).hexdigest()

    mongodb['project'].insert_one(data)
    return redirect("/admin/project/" + data['hmac'])
