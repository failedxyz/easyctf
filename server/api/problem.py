import hashlib
import logger
import os

from flask import Blueprint, jsonify, session, request
from flask import current_app as app
from werkzeug import secure_filename

from models import db, Files, Problems, Solves, Teams
from decorators import admins_only, api_wrapper, login_required

blueprint = Blueprint("problem", __name__)

@blueprint.route("/add", methods=["POST"])
@admins_only
@api_wrapper
def problem_add():
    name = request.form["name"]
    category = request.form["category"]
    description = request.form["description"]
    hint = request.form["hint"]
    flag = request.form["flag"]
    value = request.form["value"]

    name_exists = Problems.query.filter_by(name=name).first()
    if name_exists:
        return { "success":0, "message": "Problem name already taken." }

    problem = Problems(name, category, description, hint, flag, value)
    db.session.add(problem)
    db.session.commit()

    files = request.files.getlist("files[]")
    for _file in files:
        filename = secure_filename(_file.filename)

        if len(filename) == 0:
            continue

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        _file.save(file_path)
        db_file = Files(problem.pid, "/".join(file_path.split("/")[2:]))
        db.session.add(db_file)

    db.session.commit()

    return { "success": 1, "message": "Success!" }

@blueprint.route("/delete", methods=["POST"])
@admins_only
@api_wrapper
def problem_delete():
    pid = request.form["pid"]
    problem = Problems.query.filter_by(pid=pid).first()
    if problem:
        Solves.query.filter_by(pid=pid).delete()
        Challenges.query.filter_by(pid=pid).delete()
        db.session.commit()
        return { "success": 1, "message": "Success!" }
    return { "success": 0, "message": "Problem does not exist!" }

@blueprint.route("/update", methods=["POST"])
@admins_only
@api_wrapper
def problem_update():
    pid = request.form["pid"]
    name = request.form["name"]
    category = request.form["category"]
    description = request.form["description"]
    hint = request.form["hint"]
    flag = request.form["flag"]
    disabled = request.form.get("disabled", 0)
    value = request.form["value"]

    problem = Problems.query.filter_by(pid=pid).first()
    if problem:
        problem.name = name
        problem.category = category
        problem.description = description
        problem.hint = hint
        problem.flag = flag
        problem.disabled = disabled
        problem.value = value

        db.session.add(problem)
        db.session.commit()

        return { "success": 1, "message": "Success!" }
    return { "success": 0, "message": "Problem does not exist!" }

@blueprint.route("/submit", methods=["POST"])
@api_wrapper
@login_required
def problem_submit():
    pid = request.form["pid"]
    flag = request.form["flag"]
    tid = session["tid"]

    problem = Problems.query.filter_by(pid=pid).first()
    team = Teams.query.filter_by(tid=tid).first()
    if problem:
        if flag == problem.flag:
            solve = Solves(pid, tid)
            team.score += problem.value
            problem.solves += 1
            db.session.add(solve)
            db.session.add(team)
            db.session.add(problem)
            db.session.commit()

            logger.log("submissions.log", logger.WARNING, "%s has solved %s by submitting %s" % (team.name, problem.name, flag))
            return { "success": 1, "message": "Correct!" }

        else:
            logger.log("submissions.log", logger.WARNING, "%s has incorrectly submitted %s to %s" % (team.name, flag, problem.name))
            return { "success": 0, "message": "Incorrect." }

    else:
        return { "success": 0, "message": "Problem does not exist!" }

@blueprint.route("/data", methods=["POST"])
#@api_wrapper # Disable atm due to json serialization issues: will fix
@login_required
def problem_data():
    problems = Problems.query.add_columns("pid", "name", "category", "description", "hint", "value", "solves").order_by(Problems.value).filter_by(disabled=False).all()
    jason = []

    for problem in problems:
        problem_files = [ str(_file.location) for _file in Files.query.filter_by(pid=int(problem.pid)).all() ]
        jason.append({"pid": problem[1], "name": problem[2] ,"category": problem[3], "description": problem[4], "hint": problem[5], "value": problem[6], "solves": problem[7], "files": problem_files})

    return jsonify(data=jason)
