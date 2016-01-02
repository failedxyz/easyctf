import logger

from flask import Blueprint, session, request
from flask import current_app as app

from models import db, Problems, Solves, Teams
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
    description = request.form["description"]
    hint = request.form["hint"]
    flag = request.form["flag"]
    disabled = request.form["disabled"]
    value = request.form["value"]

    problem = Problems.query.filter_by(pid=pid).first()
    if problem:
        problem.name = name
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
