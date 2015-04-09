from flask import Flask, request, render_template, redirect, url_for
# from focus.model import db
from focus import loginmanager, app
from flask.ext.login import current_user, login_required, login_user, logout_user


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
    return render_template("dashboard.html")


@app.route("/admin/logout")
def logout():
    logout_user()
    return "您已经成功登出"
