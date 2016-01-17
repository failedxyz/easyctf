from flask import Blueprint, request, session
from flask import current_app as app
from voluptuous import Schema, Length, Required

from models import db, Teams, Users, TeamInvitations
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

        session["tid"] = team.tid
	return { "success": 1, "message": "Success!" }

@blueprint.route("/invite", methods=["POST"])
@api_wrapper
@login_required
def team_invite():
	params = utils.flat_multi(request.form)
	_user = user.get_user().first()
	if not user.in_team(_user):
		raise WebException("You must be in a team!")
	_team = get_team(tid=_user.tid).first()
	if _user.uid != _team.owner:
		raise WebException("You must be the captain of your team to invite members!")

	new_member = params.get("new_member")
	if new_member is None:
		raise WebException("Please provide a username!")
	_user2 = user.get_user(username_lower=new_member.lower()).first()
	if _user2 is None:
		raise WebException("User doesn't exist!")
	if _user2.tid > 0:
		raise WebException("This user is already a part of a team!")

	if _team.get_pending_invitations(toid=_user2.uid) is not None:
		raise WebException("You've already invited this member!")

	req = TeamInvitations(0, _team.tid, _user2.uid)
	with app.app_context():
		db.session.add(req)
		db.session.commit()

	return { "success": 1, "message": "Success!" }

@blueprint.route("/info", methods=["GET"])
@api_wrapper
def team_info():
	logged_in = user.is_logged_in()
	in_team = False
	owner = False
	_user = None
	search = { }
	teamname = utils.flat_multi(request.args).get("teamname")
	if teamname:
		search.update({ "teamname_lower": teamname.lower() })
	if logged_in:
		_user = user.get_user().first()
		if user.in_team(_user):
			if "teamname_lower" not in search:
				search.update({ "tid": _user.tid })
				in_team = True
	team = get_team(**search).first()
	teamdata = get_team_info(**search)
	if logged_in:
		in_team = teamdata["tid"] == _user.tid
		owner = teamdata["captain"] == _user.uid
	teamdata["in_team"] = in_team
	if in_team:
		teamdata["is_owner"] = owner
		if owner:
			teamdata["pending_invitations"] = team.get_pending_invitations()
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
	if team is None:
		raise WebException("Team not found.")

	place_number, place = team.place()
	result = {
		"tid": team.tid,
		"teamname": team.teamname,
		"school": team.school,
		"place": place,
		"place_number": place_number,
		"points": team.points(),
		"members": team.get_members(),
		"captain": team.owner,
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
