from flask import Blueprint

api = Blueprint("api", __name__)

@api.route("/api/register", methods=["POST"])
def register():
    pass

@api.route("/api/login", methods=["POST"])
def login():
    pass
