from flask.ext.sqlalchemy import SQLAlchemy
import utils

db = SQLAlchemy()

class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
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