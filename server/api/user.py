from flask import Blueprint
from utils import api_wrapper

blueprint = Blueprint("user", __name__)

@blueprint.route("/register", methods=["POST"])
@api_wrapper
def user_register():
	return { "success": 0, "message": "Registration is not open yet." }