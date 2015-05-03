from flask import request, g, jsonify, Response, json, render_template
from focus.errors import *
from focus import loginmanager, app
from flask.ext.login import current_user, login_required, login_user, logout_user
from bson.json_util import dumps
from datetime import datetime
import pickle
import hmac


def get_all_project_type():
    return [dict(name=i, title=j.TITLE) for i, j in app.blueprints.items()]
with app.app_context():
    g.get_all_project_type = get_all_project_type


@app.route("/admin/projects")
def project_management():
    return render_template("project_list.html")


@app.route("/admin/project/<project>")
@app.route("/admin/project", defaults={"project": None})
@login_required
def project_operation(project):
    if project:
        # return the info of single project
        data = g.mongodb['meta'].find_one({"hmac": project})
        return render_template("project_overview.html", data=data, pid=project)
    else:
        # return general infomation
        return 'projects overview'


def validType(type_name):
    if type_name in [i['name'] for i in get_all_project_type()]:
        return type_name
    else:
        raise WrongPostData(1, "错误的参数")


@app.route('/test')
def test():
    #DELETEME
    data = [dict(name=i, title=j.TITLE) for i, j in app.blueprints.items()]
    return Response(json.dumps(data), mimetype="application/json")


@app.route("/admin/api/new_project", methods=["POST"])
def new_project_api():
    data = {
        "project_type": validType(request.form['project_type']),
        "comment": request.form.get('comment', ''),
        "time": datetime.now(),
        "name": request.form['project_name']
    }
    data['hmac'] = hmac.new(pickle.dumps(data)).hexdigest()

    g.mongodb['meta'].insert_one(data)
    return jsonify(
        id=data['hmac'],
        err=0
    )
