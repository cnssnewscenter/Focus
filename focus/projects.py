from flask import Flask, request, render_template, redirect, url_for
# from focus.model import db
from focus import loginmanager, app
from flask.ext.login import current_user, login_required, login_user, logout_user


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


@app.route("/admin/api/new")
def new_project_api():
    data = {
        "project_type": request.form['project_type'],
        "comment": request.form.get('comment', ''),
    }
    

