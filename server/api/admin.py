from flask import Blueprint, jsonify
from decorators import admins_only, api_wrapper, login_required
from models import db, Problems, Files

blueprint = Blueprint("admin", __name__)

@blueprint.route("/problem/data", methods=["POST"])
#@api_wrapper # Disable atm due to json serialization issues: will fix
@admins_only
@login_required
def problem_data():
    problems = Problems.query.add_columns("pid", "name", "category", "description", "hint", "value", "solves", "disabled", "flag").order_by(Problems.value).all()
    jason = []

    for problem in problems:
        problem_files = [ str(_file.location) for _file in Files.query.filter_by(pid=int(problem.pid)).all() ]
        jason.append({"pid": problem[1], "name": problem[2] ,"category": problem[3], "description": problem[4], "hint": problem[5], "value": problem[6], "solves": problem[7], "disabled": problem[8], "flag": problem[9], "files": problem_files})

    return jsonify(data=jason)
