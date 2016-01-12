from flask import Blueprint, jsonify
from decorators import admins_only, api_wrapper
from models import db, Problems, Files

import json

blueprint = Blueprint("admin", __name__)

@blueprint.route("/problems/list", methods=["GET"])
@api_wrapper
@admins_only
def problem_data():
	problems = Problems.query.order_by(Problems.value).all()
	problems_return = [ ]
	for problem in problems:
		problems_return.append({
			"pid": problem.pid,
			"name": problem.name,
			"category": problem.category,
			"description": problem.description,
			"hint": problem.hint,
			"value": problem.value,
			"threshold": problem.threshold,
			"weightmap": json.loads(problem.weightmap)
		})
	return { "success": 1, "problems": problems_return }