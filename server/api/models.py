from flask.ext.sqlalchemy import SQLAlchemy

import time
import traceback
import utils

db = SQLAlchemy()

class Users(db.Model):
	uid = db.Column(db.Integer, unique=True, primary_key=True)
	tid = db.Column(db.Integer)
	name = db.Column(db.String(64))
	username = db.Column(db.String(64), unique=True)
	username_lower = db.Column(db.String(64), unique=True)
	email = db.Column(db.String(64), unique=True)
	password = db.Column(db.String(128))
	admin = db.Column(db.Boolean)
	utype = db.Column(db.Integer)
	tid = db.Column(db.Integer)
	registertime = db.Column(db.Integer)

	def __init__(self, name, username, email, password, utype=1):
		self.name = name
		self.username = username
		self.username_lower = username.lower()
		self.email = email.lower()
		self.password = utils.hash_password(password)
		self.utype = utype
		self.admin = False
		self.registertime = int(time.time())

class Teams(db.Model):
	tid = db.Column(db.Integer, primary_key=True)
	teamname = db.Column(db.String(64), unique=True)
	teamname_lower = db.Column(db.String(64), unique=True)
	school = db.Column(db.Text)
	owner = db.Column(db.Integer)
	observer = db.Column(db.Boolean)

	def __init__(self, teamname, school, owner, observer):
		self.teamname = teamname
		self.teamname_lower = teamname.lower()
		self.school = school
		self.owner = owner
		self.observer = observer

	def get_members(self):
		members = [ ]
		for member in Users.query.filter_by(tid=self.tid).all():
			members.append({
				"username": member.username,
				"name": member.name,
				"captain": member.uid == self.owner
			})
		return members

	def points(self):
		score = db.func.sum(Problems.value).label("score")
		team = db.session.query(Solves.tid, score).join(Teams).join(Problems).filter(Teams.tid==self.tid).group_by(Solves.tid).first()
		if team:
			return team.score
		else:
			return 0

	def place(self):
		score = db.func.sum(Problems.value).label("score")
		quickest = db.func.max(Solves.date).label("quickest")
		teams = db.session.query(Solves.tid).join(Teams).join(Problems).filter().group_by(Solves.tid).order_by(score.desc(), quickest).all()
		try:
			i = teams.index((self.tid,)) + 1
			k = i % 10
			return (i, "%d%s" % (i, "tsnrhtdd"[(i / 10 % 10 != 1) * (k < 4) * k::4]))
		except ValueError:
			return (-1, "--")

	def get_pending_invitations(self, toid=None):
		if toid is not None:
			invitation = db.session.query(TeamInvitations).filter_by(rtype=0, frid=self.tid, toid=toid).first()
			if invitation is None:
				return None
			else:
				user = db.session.query(Users).filter_by(uid=invitation.toid).first()
				return { "username": user.username, "name": user.name, "uid": user.uid }
		result = [ ]
		invitations = db.session.query(TeamInvitations).filter_by(rtype=0, frid=self.tid).all()
		for invitation in invitations:
			user = db.session.query(Users).filter_by(uid=invitation.toid).first()
			result.append({
				"username": user.username,
				"name": user.name,
				"uid": user.uid
			})
		return result

class Problems(db.Model):
	pid = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128))
	category = db.Column(db.String(128))
	description = db.Column(db.Text)
	hint = db.Column(db.Text)
	flag = db.Column(db.Text)
	disabled = db.Column(db.Boolean, default=False)
	value = db.Column(db.Integer)
	solves = db.Column(db.Integer, default=0)

	def __init__(self, name, category, description, hint, flag, value):
		self.name = name
		self.category = category
		self.description = description
		self.hint = hint
		self.flag = flag
		self.value = value

class Files(db.Model):
	fid = db.Column(db.Integer, primary_key=True)
	pid = db.Column(db.Integer)
	location = db.Column(db.Text)

	def __init__(self, pid, location):
		self.pid = pid
		self.location = location

class Solves(db.Model):
	sid = db.Column(db.Integer, primary_key=True)
	pid = db.Column(db.Integer, db.ForeignKey("problems.pid"))
	tid = db.Column(db.Integer, db.ForeignKey("teams.tid"))
	date = db.Column(db.Integer, default=utils.get_time_since_epoch())
	team = db.relationship("Teams", foreign_keys="Solves.tid", lazy="joined")
	prob = db.relationship("Problems", foreign_keys="Solves.pid", lazy="joined")
	correct = db.Column(db.Boolean)
	flag = db.Column(db.Text)

	def __init__(self, pid, tid, flag, correct):
		self.pid = pid
		self.tid = tid
		self.flag = flag
		self.correct = correct

class LoginTokens(db.Model):
	sid = db.Column(db.String(64), unique=True, primary_key=True)
	uid = db.Column(db.Integer)
	username = db.Column(db.String(32))
	active = db.Column(db.Boolean)
	issued = db.Column(db.Integer)
	expiry = db.Column(db.Integer)
	ua = db.Column(db.String(128))
	ip = db.Column(db.String(16))

	def __init__(self, uid, username, expiry=int(time.time()), active=True, ua=None, ip=None):
		self.sid = utils.generate_string()
		self.uid = uid
		self.username = username
		self.issued = int(time.time())
		self.expiry = expiry
		self.active = active
		self.ua = ua
		self.ip = ip

class TeamInvitations(db.Model):
	rid = db.Column(db.Integer, primary_key=True)
	rtype = db.Column(db.Integer)
	frid = db.Column(db.Integer)
	toid = db.Column(db.Integer)
	date = db.Column(db.Integer, default=utils.get_time_since_epoch())

	def __init__(self, rtype, frid, toid):
		self.rtype = rtype
		self.frid = frid
		self.toid = toid