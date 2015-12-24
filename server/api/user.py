from flask import Blueprint, session
from utils import api_wrapper

blueprint = Blueprint("user", __name__)

@blueprint.route("/register", methods=["POST"])
@api_wrapper
def user_register():
	return { "success": 0, "message": "Registration is not open yet." }

@blueprint.route("/logout", methods=["POST"])
@api_wrapper
def user_logout():
    # session.clear()
    pass

@blueprint.route("/login", methods=["POST"])
@api_wrapper
def user_login():
    pass
