from flask import Blueprint, session, request
from flask import current_app as app

from models import db, Users
from utils import api_wrapper

import utils

blueprint = Blueprint("user", __name__)

@blueprint.route("/register", methods=["POST"])
@api_wrapper
def user_register():
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]
    password_confirm = request.form["password_confirm"]
    email = request.form["email"]

    username_exists = Users.query.add_columns("name", "uid").filter_by(username_lower=username.lower()).first()
    email_exists = Users.query.add_columns("name", "uid").filter_by(email=email).first()

    if password != password_confirm:
        return { "success": 0, "message": "Passwords do not match." }
    if len(password) > 128:
        return { "success": 0, "message": "Password is too long." }
    if len(password) == 0:
        return { "success": 0, "message": "Password is too short." }
    if len(username) > 64:
        return { "success": 0, "message": "Username is too long." }
    if username_exists:
        return { "success": 0, "message": "Username is already taken." }
    if email_exists:
        return { "success": 0, "message": "Email has already been used." }

    add_user(name, username, email, password)

    return { "success": 1, "message": "Success!" }

@blueprint.route("/logout", methods=["POST"])
@api_wrapper
def user_logout():
    session.clear()

@blueprint.route("/login", methods=["POST"])
@api_wrapper
def user_login():
    username = request.form["username"]
    password = request.form["password"]
    user = Users.query.filter_by(username=username).first()
    if utils.check_password(user.password, password):
        session["username"] = username
        session["admin"] = user.admin
        return { "success": 1, "message": "Success!" }
    else:
        return { "success": 0, "message": "Invalid credentials." }

def add_user(name, username, email, password):
    user = Users(name, username, email, password)
    db.session.add(user)
    db.session.commit()
