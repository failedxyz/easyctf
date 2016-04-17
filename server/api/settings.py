from flask import Blueprint, request

from models import db, Settings
from decorators import admins_only, api_wrapper, WebException

blueprint = Blueprint("setting", __name__)

@blueprint.route("/update", methods=["POST"])
@admins_only
@api_wrapper
def update_setting():
	for key in request.form.keys():
		value = request.form[key]
		set(key, value)
	return { "success": 1, "message": "Success!" }

def set(key, value):
	setting = Settings.query.filter_by(key=key).first()
	if setting:
		setting.value = value
	else:
		setting = Settings(key, value)
		db.session.add(setting)
	db.session.commit()
	return setting

def get_all():
	settings = {}
	for setting in Settings.query.all():
		settings[setting.key] = setting.value

def get(key):
	setting = Settings.query.filter_by(key=key).first()
	if setting:
		return setting.value
	return set(key, None)
