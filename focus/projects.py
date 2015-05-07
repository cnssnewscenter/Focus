from flask import request, g, render_template
from focus.errors import *
from focus import app, mongodb, views
from flask.ext.login import login_required
from datetime import datetime
import pickle
import hmac
import logging


def get_all_project_type():
    return [dict(name=i, title=j.TITLE) for i, j in app.blueprints.items()]
with app.app_context():
    g.get_all_project_type = get_all_project_type


@app.route("/admin/projects")
@login_required
def project_management():
    projects = list(mongodb['meta'].find())
    return render_template("project_list.html", projects=projects)


@app.route("/admin/project/<project>")
@app.route("/admin/project", defaults={"project": None})
@login_required
def project_operation(project):
    if project:
        # return the info of single project
        data = mongodb['meta'].find_one({"hmac": project})
        return render_template("project_overview.html", data=data, pid=project)
    else:
        # return general infomation
        return 'projects overview'


def validType(type_name):
    if type_name in [i['name'] for i in get_all_project_type()]:
        return type_name
    else:
        raise WrongPostData(1, "错误的参数")


@app.route("/admin/api/new_project", methods=["POST"])
@login_required
def new_project_api():
    data = {
        "project_type": validType(request.form['project_type']),
        "comment": request.form.get('comment', ''),
        "time": datetime.now(),
        "name": request.form['project_name'],
        "click": 0
    }
    data['hmac'] = hmac.new(pickle.dumps(data)).hexdigest()

    mongodb['meta'].insert_one(data)
    update_routes()
    return jsonify(
        id=data['hmac'],
        err=0
    )


def update_routes():
    for i in mongodb.meta.find():
        logging.info('config the %s', i.hmac)
        try:
            getattr(views, i.project_type).new_url(i.hmac)
        except Exception as err:
            logging.error("meet error %s", err.with_traceback())
        logging.info('successfully config the %s', i.hmac)
