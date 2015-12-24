from flask.ext.sqlalchemy import SQLAlchemy
import utils

db = SQLAlchemy()

class Users(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    tid = db.Column(db.Integer)
    name = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True)
    username_lower = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    admin = db.Column(db.Boolean)

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.username_lower = username.lower()
        self.email = email.lower()
        self.password = utils.hash_password(password)

class Teams(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    join_code = db.Column(db.String(128), unique=True)
    school = db.Column(db.Text)
    size = db.Column(db.Integer)
    score = db.Column(db.Integer)
    observer = db.Column(db.Boolean)
    owner = db.Column(db.Integer)

    def __init__(self, name, school):
        self.name = name
        self.school = school

class Problems(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text)
    hint = db.Column(db.Text)
    flag = db.Column(db.Text)
    disabled = db.Column(db.Boolean)
    value = db.Column(db.Integer)
    solves = db.Column(db.Integer)

    def __init__(self, name, description, hint, flag, value):
        self.name = name
        self.description = description
        self.hint = hint
        self.flag = flag
        self.value = value

class Solves(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    tid = db.Column(db.Integer)
    date = db.Column(db.Integer, default=utils.get_time_since_epoch())

    def __init__(self, pid, tid):
        self.pid = pid
        self.tid = tid
