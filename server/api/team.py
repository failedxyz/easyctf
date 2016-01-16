from flask import Blueprint, request
from flask import current_app as app
from voluptuous import Schema, Length, Required

from models import db, Teams, Users
from decorators import api_wrapper, login_required, WebException
from schemas import verify_to_schema, check

import user
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
	_user = user.get_user().first()
	if _user.tid is not None or _user.tid >= 0 or get_team(owner=_user.uid).first() is not None:
		raise WebException("You're already in a team!")

	verify_to_schema(TeamSchema, params)
	teamname = params.get("teamname")
	school = params.get("school")

	team = Teams(teamname, school, _user.uid, _user.utype != 1)
	with app.app_context():
		db.session.add(team)
		db.session.commit()
		Users.query.filter_by(uid=_user.uid).update({ "tid": team.tid })
		db.session.commit()
	
	return { "success": 1, "message": "Success!" }

@blueprint.route("/info", methods=["GET"])
@api_wrapper
def team_info():
	logged_in = user.is_logged_in()
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
		"teamname": team.teamname,
		"school": team.school
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
	Required("school"): check(
		([str, Length(min=4, max=60)], "Your school name should be between 4 and 60 characters long."),
		([utils.__check_ascii], "Please only use ASCII characters in your school name."),
	),
}, extra=True)

def get_team_info(tid=None, teamname=None, teamname_lower=None, owner=None):
	team = get_team(tid=tid, teamname=teamname, teamname_lower=teamname_lower, owner=owner).first()
	place_number, place = team.place()
	result = {
		"tid": team.tid,
		"teamname": team.teamname,
		"school": team.school,
		"place": place,
		"place_number": place_number,
		"points": team.points()
	}
	return result

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
	elif user.is_logged_in():
		_user = user.get_user().first()
		if _user.tid is not None:
			match.update({ "tid": _user.tid })
	with app.app_context():
		result = Teams.query.filter_by(**match)
		return result