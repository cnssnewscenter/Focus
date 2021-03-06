from flask import request, render_template, redirect, url_for, send_from_directory, abort, jsonify
from focus import loginmanager, app, mongodb
from focus.errors import WrongPostData
from flask.ext.login import current_user, login_required, login_user, logout_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from bson.objectid import ObjectId
import math
import pymongo

class User():

    """
    The user proxy for flask-login
    """

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return "admin"

user = User()

@loginmanager.user_loader
def load_user(userid):
    return User()


@app.route("/admin/")
def index():
    if current_user.is_authenticated():
        return redirect("/admin/dashboard")
    else:
        return redirect(url_for(".login"))
        # jump to login


@app.route("/admin/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated():
            return redirect(url_for(".dashboard"))
        else:
            return render_template("login.html")
    elif request.method == "POST":
        if app.config['ADMIN_USER'] == request.form.get('username') \
                and app.config["ADMIN_PWD"] == request.form.get("password"):
            login_user(user)
            return redirect(url_for(".dashboard"))
        else:
            # TODO add try times limit
            return render_template("login.html", err_msg="错误的用户名/密码组合")


@app.route("/admin/dashboard")
@login_required
def dashboard():
    # gathering the projects infomation
    data = {
        "project_number": mongodb.meta.projects.count(),
        "total_click": 0,
        "new_click": 0
    }
    return render_template("dashboard.html", data=data)


@app.route("/admin/logout")
def logout():
    logout_user()
    return "您已经成功登出"


@app.route("/admin/project/new")
@login_required
def new_project():
    project_types = [dict(name=i, title=j.TITLE) for i, j in app.blueprints.items()]
    return render_template("new_project.html", project_types=project_types)


@app.route("/admin/config")
@login_required
def general_config():
    return render_template('site_config.html')


@app.route("/debugger")
def debugger():
    raise


def allow(filename):
    return "." in filename and filename.lower().rsplit('.', 1)[1] in app.config['UPLOAD_ALLOWED']


@app.route("/admin/upload", methods=["POST"])
# @login_required
def upload():
    file = request.files['file']
    print(file.filename)
    if file and allow(file.filename):
        filename = secure_filename(file.filename)
        t = datetime.now()
        new_filename = str(int(t.timestamp() * 1000)) + os.path.splitext(filename)[1]
        path = os.path.join(str(t.year), str(t.month), new_filename)
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], path)
        # make the folder
        print(path, saved_path, os.getcwd())
        os.makedirs(os.path.split(saved_path)[0], exist_ok=True)

        file.save(saved_path)
        # and save this to the database
        record = mongodb['upload'].insert_one({
            "path": path,
            "time": t,
            "size": int(os.stat(saved_path).st_size),
            "name": file.filename
        })
        return jsonify(
            err=0,
            fid=str(record.inserted_id)
        )
    else:
        raise WrongPostData(1, "no avaliable file uploaded")

@app.route("/f/<fid>")
def uploaded_file(fid):
    try:
        file = mongodb.upload.find_one({"_id": ObjectId(fid)})
        if file:
            return send_from_directory(app.config['UPLOAD_FOLDER'], file['path'])
        else:
            abort(404)
    except:
        abort(404)

@app.route('/admin/uploader')
@login_required
def upload_overview():
    return render_template("upload.html")

@app.route("/admin/uploads")
# @login_required
def api_uploads():
    page = int(request.args.get("p", 1))
    if page <= 0:
        page = 1
    ret = list(mongodb.upload.find().sort("time", pymongo.DESCENDING).skip(50 * (page - 1)).limit(50))
    for i in ret:
        i['id'] = str(i.pop('_id'))
    all_length = math.ceil(mongodb.upload.count() / 50)
    return jsonify(
        data=ret,
        all=all_length
    )