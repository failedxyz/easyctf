from flask import Blueprint, request, session
from flask import current_app as app

from decorators import api_wrapper

import team

blueprint = Blueprint("stats", __name__)

@blueprint.route("/scoreboard")
@api_wrapper
def all_teams_stats():
	teams = team.get_team().all()
	result = [ ]
	for _team in teams:
		result.append({
			"teamname": _team.teamname,
			"tid": _team.tid,
			"school": _team.school,
			"points": _team.points()
		})
	return { "success": 1, "scoreboard": result }