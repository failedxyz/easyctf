from flask import Blueprint, session, request, redirect, url_for
from flask import current_app as app
from voluptuous import Schema, Length, Required

from models import db, LoginTokens, Users
from decorators import api_wrapper, WebException
from schemas import verify_to_schema, check

import datetime
import logger
import re
import requests
import utils

###############
# USER ROUTES #
###############

blueprint = Blueprint("user", __name__)

@blueprint.route("/register", methods=["POST"])
@api_wrapper
def user_register():
	params = utils.flat_multi(request.form)

	name = params.get("name")
	email = params.get("email")
	username = params.get("username")
	password = params.get("password")
	password_confirm = params.get("password_confirm")
	utype = int(params.get("type"))

	if password != password_confirm:
		raise WebException("Passwords do not match.")
	verify_to_schema(UserSchema, params)

	user = Users(name, username, email, password, utype)
	with app.app_context():
		db.session.add(user)
		db.session.commit()

	logger.log("registrations", logger.INFO, "%s registered with %s" % (name.encode("utf-8"), email.encode("utf-8")))
	login_user(username, password)

	return { "success": 1, "message": "Success!" }

@blueprint.route("/logout", methods=["POST"])
@api_wrapper
def user_logout():
	sid = session["sid"]
	username = session["username"]
	with app.app_context():
		expired = LoginTokens.query.filter_by(username=username).all()
		for expired_token in expired: db.session.delete(expired_token)
		db.session.commit()
	session.clear()

@blueprint.route("/login", methods=["POST"])
@api_wrapper
def user_login():
	params = utils.flat_multi(request.form)

	username = params.get("username")
	password = params.get("password")

	result = login_user(username, password)
	if result != True:
		raise WebException("Please check if your username/password are correct.")

	return { "success": 1, "message": "Success!" }

@blueprint.route("/status", methods=["POST"])
@api_wrapper
def user_status():
	logged_in = is_logged_in()
	result = {
		"success": 1,
		"logged_in": logged_in,
		"admin": is_admin(),
		"username": session["username"] if logged_in else "",
	}
	return result

@blueprint.route("/info", methods=["POST"])
@api_wrapper
def user_info():
	logged_in = is_logged_in()
	username = utils.flat_multi(request.form).get("username")
	if username is None:
		if logged_in:
			username = session["username"]
	if username is None:
		raise WebException("No user specified.")
	me = False if not("username" in session) else username.lower() == session["username"].lower()
	user = get_user(username_lower=username.lower()).first()
	if user is None:
		raise WebException("User not found.")

	show_email = me if logged_in else False
	userdata = {
		"user_found": True,
		"name": user.name,
		"username": user.username,
		"type": ["Student", "Instructor", "Observer"][user.utype - 1],
		"admin": user.admin,
		"registertime": datetime.datetime.fromtimestamp(user.registertime).isoformat() + "Z",
		"me": me,
		"show_email": show_email
	}
	if show_email:
		userdata["email"] = user.email
	return { "success": 1, "user": userdata }

##################
# USER FUNCTIONS #
##################

__check_email_format = lambda email: re.match(".+@.+\..{2,}", email) is not None
__check_ascii = lambda s: all(ord(c) < 128 for c in s)
__check_username = lambda username: get_user(username_lower=username.lower()).first() is None
__check_email = lambda email: get_user(email=email.lower()).first() is None

UserSchema = Schema({
	Required("email"): check(
		([str, Length(min=4, max=128)], "Your email should be between 4 and 128 characters long."),
		([__check_email], "Someone already registered this email."),
		([__check_email_format], "Please enter a legit email.")
	),
	Required("name"): check(
		([str, Length(min=4, max=128)], "Your name should be between 4 and 128 characters long.")
	),
	Required("username"): check(
		([str, Length(min=4, max=32)], "Your username should be between 4 and 32 characters long."),
		([__check_ascii], "Please only use ASCII characters in your username."),
		([__check_username], "This username is taken, did you forget your password?")
	),
	Required("password"): check(
		([str, Length(min=4, max=64)], "Your password should be between 4 and 64 characters long."),
		([__check_ascii], "Please only use ASCII characters in your password."),
	),
	Required("type"): check(
		([str, lambda x: x.isdigit()], "Please use the online form.")
	),
	"notify": str
}, extra=True)

def get_user(username=None, username_lower=None, email=None, uid=None):
	match = {}
	if username != None:
		match.update({ "username": username })
	elif username_lower != None:
		match.update({ "username_lower": username_lower })
	elif uid != None:
		match.update({ "uid": uid })
	elif email != None:
		match.update({ "email": email })
	# elif api.auth.is_logged_in():
	# 	match.update({ "uid": api.auth.get_uid() })
	with app.app_context():
		result = Users.query.filter_by(**match)
		return result

def login_user(username, password):
	user = get_user(username_lower=username.lower()).first()
	if user is None: return False
	correct = utils.check_password(user.password, password)
	if not correct: return False

	useragent = request.headers.get("User-Agent")
	ip = request.remote_addr

	with app.app_context():
		expired = LoginTokens.query.filter_by(username=username).all()
		for expired_token in expired: db.session.delete(expired_token)

		token = LoginTokens(user.uid, user.username, ua=useragent, ip=ip)
		db.session.add(token)
		db.session.commit()
			
		session["sid"] = token.sid
		session["username"] = token.username
		session["admin"] = user.admin == True

	return True

def is_logged_in():
	if not("sid" in session and "username" in session): return False
	sid = session["sid"]
	username = session["username"]
	token = LoginTokens.query.filter_by(sid=sid).first()
	if token is None: return False

	useragent = request.headers.get("User-Agent")
	ip = request.remote_addr

	if token.username != username: return False
	if token.ua != useragent: return False
	return True

def is_admin():
	return is_logged_in() and "admin" in session and session["admin"]

def validate_captcha(form):
	if "captcha_response" not in form:
		return False
	captcha_response = form["captcha_response"]
	data = {"secret": "6Lc4xhMTAAAAACFaG2NyuKoMdZQtSa_1LI76BCEu", "response": captcha_response}
	response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
	return response.json()["success"]