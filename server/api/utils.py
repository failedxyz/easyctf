import datetime
import json
import random
import string
import traceback

from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

class WebException(Exception): pass

def hash_password(s):
	return generate_password_hash(s)

def check_password(hashed_password, try_password):
	return check_password_hash(hashed_password, try_password)

def generate_string(length):
	return "".join([random.choice(string.letters + string.digits) for x in range(length)])

def unix_time_millis(dt):
	epoch = datetime.datetime.utcfromtimestamp(0)
	return (dt - epoch).total_seconds() * 1000.0

def get_time_since_epoch():
	return unix_time_millis(datetime.datetime.now())

def api_wrapper(f):
	@wraps(f)
	def wrapper(*args, **kwds):
		web_result = {}
		response = 200
		try:
			web_result = f(*args, **kwds)
		except WebException as error:
			response = 200
			web_result = { "success": 0, "message": str(error) }
		except Exception as error:
			response = 200
			traceback.print_exc()
			web_result = { "success": 0, "message": "Something went wrong! Please notify us about this immediately.", error: traceback.format_exc() }
		return json.dumps(web_result), response, { "Content-Type": "application/json; charset=utf-8" }
	return wrapper
