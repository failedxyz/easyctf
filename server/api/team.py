from flask import Blueprint, request
from flask import current_app as app
from voluptuous import Schema, Length, Required

from models import db, Teams, Users
from decorators import api_wrapper, login_required, WebException
from user import in_team, get_user, is_logged_in
from schemas import verify_to_schema, check

import utils

blueprint = Blueprint("team", __name__)

###############
# TEAM ROUTES #
###############

@blueprint.route("/create", methods=["POST"])
@api_wrapper
@login_required
def team_create():
	params = utils.flat_multi(request.form)
	user = get_user().first()
	if user.tid is not None or user.tid >= 0 or get_team(owner=user.uid).first() is not None:
		raise WebException("You're already in a team!")

	verify_to_schema(TeamSchema, params)
	teamname = params.get("teamname")

	team = Teams(teamname, user.uid)
	with app.app_context():
		db.session.add(team)
		db.session.commit()
		Users.query.filter_by(uid=user.uid).update({ "tid": team.tid })
		db.session.commit()
	
	return { "success": 1, "message": "Success!" }

@blueprint.route("/info", methods=["GET"])
@api_wrapper
def team_info():
	logged_in = is_logged_in()
	me = False 
	teamname = utils.flat_multi(request.args).get("teamname")
	if logged_in:
		my_team = get_team().first()
		if my_team is not None:
			if teamname is None:
				teamname = my_team.teamname
				me = True
			elif teamname.lower() == my_team.teamname.lower():
				me = True
	if teamname is None:
		raise WebException("No team specified.")
	team = get_team(teamname_lower=teamname.lower()).first()
	if team is None:
		raise WebException("Team not found.")

	teamdata = {
		"teamname": team.teamname
	}
	teamdata["in_team"] = me
	return { "success": 1, "team": teamdata }

##################
# TEAM FUNCTIONS #
##################

__check_teamname = lambda teamname: get_team(teamname_lower=teamname.lower()).first() is None

TeamSchema = Schema({
	Required("teamname"): check(
		([str, Length(min=4, max=32)], "Your teamname should be between 4 and 32 characters long."),
		([utils.__check_ascii], "Please only use ASCII characters in your teamname."),
		([__check_teamname], "This teamname is taken, did you forget your password?")
	),
}, extra=True)

def get_team(tid=None, teamname=None, teamname_lower=None, owner=None):
	match = {}
	if teamname != None:
		match.update({ "teamname": teamname })
	elif teamname_lower != None:
		match.update({ "teamname_lower": teamname_lower })
	elif tid != None:
		match.update({ "tid": tid })
	elif owner != None:
		match.update({ "owner": owner })
	elif is_logged_in():
		user = get_user().first()
		if user.tid is not None:
			match.update({ "tid": user.tid })
	with app.app_context():
		result = Teams.query.filter_by(**match)
		return result