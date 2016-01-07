import datetime
import json
import random
import string
import traceback
import unicodedata

from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(s):
	return generate_password_hash(s)

def check_password(hashed_password, try_password):
	return check_password_hash(hashed_password, try_password)

def generate_string(length=32, alpha=string.hexdigits):
	return "".join([random.choice(alpha) for x in range(length)])

def unix_time_millis(dt):
	epoch = datetime.datetime.utcfromtimestamp(0)
	return (dt - epoch).total_seconds() * 1000.0

def get_time_since_epoch():
	return unix_time_millis(datetime.datetime.now())

def flat_multi(multidict):
	flat = {}
	for key, values in multidict.items():
		value = values[0] if type(values) == list and len(values) == 1 else values
		flat[key] = unicodedata.normalize("NFKD", value).encode("ascii", "ignore")
	return flat