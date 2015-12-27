from flask import Blueprint, session, request
from flask import current_app as app

from models import db, Users
from decorators import api_wrapper

import logging
import requests
import utils

blueprint = Blueprint("user", __name__)

@blueprint.route("/register", methods=["POST"])
@api_wrapper
def user_register():
	if not validate_captcha(request.form):
		return { "success": 0, "message": "Please do the captcha." }

	name = request.form["name"]
	username = request.form["username"]
	password = request.form["password"]
	password_confirm = request.form["password_confirm"]
	email = request.form["email"]

	username_exists = Users.query.add_columns("name", "uid").filter_by(username_lower=username.lower()).first()
	email_exists = Users.query.add_columns("name", "uid").filter_by(email=email.lower()).first()

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
	logger = logging.getLogger("regs")
	logger.warn("[{0}] {1} registered with {2}".format(time.strftime("%m/%d/%Y %X"), name.encode("utf-8"), email.encode("utf-8")))

	return { "success": 1, "message": "Success!" }

@blueprint.route("/logout", methods=["POST"])
@api_wrapper
def user_logout():
	session.clear()

@blueprint.route("/login", methods=["POST"])
@api_wrapper
def user_login():
	email = request.form["email"]
	password = request.form["password"]
	user = Users.query.filter_by(email=email).first()
	if user is None:
		return { "success": 0, "message": "Invalid credentials." }

	if utils.check_password(user.password, password):
		session["username"] = user.username
		session["admin"] = user.admin
		session["logged_in"] = True
		return { "success": 1, "message": "Success!" }
	else:
		return { "success": 0, "message": "Invalid credentials." }

def add_user(name, username, email, password):
	user = Users(name, username, email, password)
	db.session.add(user)
	db.session.commit()

def validate_captcha(form):
	if "captcha_response" not in form:
		return False
	captcha_response = form["captcha_response"]
	data = {"secret": "6Lc4xhMTAAAAACFaG2NyuKoMdZQtSa_1LI76BCEu", "response": captcha_response}
	response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
	if response.json()["success"]:
		return True
	return False
